import os
import datetime
import json
from typing import List, Dict, Optional, Union, Any
import re
import random
from datetime import datetime, timedelta

# For calendar integration
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class PamBot:
    """
    Pam Bot: The central coordinator for the Dunder Mifflin agent ecosystem.
    Handles scheduling, reminders, and communication between agents.
    """
    
    def __init__(self, config_path: str = "pam_config.json"):
        """Initialize Pam Bot with configuration"""
        self.name = "Pam Beesly"
        self.role = "Reception & Coordination"
        self.catchphrases = [
            "Dunder Mifflin, this is Pam.",
            "I'll transfer you now.",
            "Yep.",
            "Hey guys!",
            "Let me check the calendar for you."
        ]
        
        # Load or create configuration
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize calendar service (if available)
        self.calendar_service = None
        if GOOGLE_AVAILABLE and self.config.get("use_google_calendar", False):
            self._setup_google_calendar()
        
        # Initialize state trackers
        self.appointments = self.config.get("appointments", [])
        self.reminders = self.config.get("reminders", [])
        self.agent_registry = self.config.get("agents", {})
        self.conversation_history = []
        
        print(f"{self.name} initialized and ready to coordinate!")
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration or create default if not exists"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading config, creating new one.")
        
        # Default configuration
        default_config = {
            "use_google_calendar": True,
            "google_calendar_id": "primary",
            "token_path": "token.json",
            "credentials_path": "credentials.json",
            "appointments": [],
            "reminders": [],
            "agents": {}
        }
        
        # Save default configuration
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
    
    def _save_config(self) -> None:
        """Save current configuration to file"""
        # Update config with current state
        self.config["appointments"] = self.appointments
        self.config["reminders"] = self.reminders
        self.config["agents"] = self.agent_registry
        
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def _setup_google_calendar(self) -> None:
        """Set up Google Calendar integration"""
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        token_path = self.config.get("token_path")
        credentials_path = self.config.get("credentials_path")
        
        # Load token if it exists
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_info(
                json.loads(open(token_path).read()), SCOPES)
                
        # Refresh or get new credentials if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    print("Error: credentials.json is missing. Please set up Google Calendar API credentials.")
                    return
                    
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                
        try:
            self.calendar_service = build('calendar', 'v3', credentials=creds)
            print("Google Calendar integration active.")
        except Exception as e:
            print(f"Failed to set up Google Calendar: {str(e)}")
    
    def respond(self, message: str, context: Dict[str, Any] = None) -> str:
        """Generate a response based on the input message"""
        # Track conversation
        if context and 'user' in context:
            self.conversation_history.append({
                'from': context['user'],
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
        
        # Simple intent detection
        message_lower = message.lower()
        
        # Check for scheduling intents
        if any(word in message_lower for word in ["schedule", "appointment", "meeting", "book"]):
            return self._handle_scheduling(message)
            
        # Check for reminder intents
        elif any(word in message_lower for word in ["remind", "reminder", "don't forget"]):
            return self._handle_reminder(message)
            
        # Check for calendar query intents
        elif any(word in message_lower for word in ["calendar", "schedule", "free", "available"]):
            return self._handle_calendar_query(message)
            
        # Default receptionist response
        else:
            return self._receptionist_response(message)
    
    def _receptionist_response(self, message: str) -> str:
        """Default receptionist response"""
        greetings = ["Hello!", "Hi there!", "Dunder Mifflin, this is Pam."]
        waiting_responses = ["One moment please.", "Let me check that for you.", "I'll see what I can do."]
        farewell = ["Is there anything else I can help with?", "Let me know if you need anything else.", "Anything else?"]
        
        return f"{random.choice(greetings)} {random.choice(waiting_responses)} {random.choice(farewell)}"
    
    def _handle_scheduling(self, message: str) -> str:
        """Handle scheduling-related requests"""
        # Extract date and time using regex
        date_pattern = r'\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|\d{1,2}[-/]\d{1,2}(?:[-/]\d{2,4})?)\b'
        time_pattern = r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b'
        
        date_match = re.search(date_pattern, message.lower())
        time_match = re.search(time_pattern, message.lower())
        
        title_pattern = r'(?:for|about|with|regarding)\s+(.*?)(?:\bat\b|\bon\b|from|\d{1,2}|\.$|$)'
        title_match = re.search(title_pattern, message.lower())
        
        if date_match and time_match:
            date_str = date_match.group(1)
            time_str = time_match.group(1)
            title = title_match.group(1).strip() if title_match else "Untitled Meeting"
            
            # Add the appointment
            appointment = {
                'title': title,
                'date': date_str,
                'time': time_str,
                'created': datetime.now().isoformat()
            }
            
            self.appointments.append(appointment)
            self._save_config()
            
            # If Google Calendar is available, add it there too
            if self.calendar_service:
                self._add_to_google_calendar(appointment)
            
            return f"I've scheduled '{title}' for {date_str} at {time_str}. It's on the calendar!"
        else:
            return "I couldn't understand the date and time. Could you provide them in a clearer format? For example: 'Schedule a meeting with Michael tomorrow at 2pm.'"
    
    def _handle_reminder(self, message: str) -> str:
        """Handle reminder-related requests"""
        # Extract time information
        time_pattern = r'\b(today|tomorrow|in \d+ (?:minute|hour|day)s?|at \d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b'
        time_match = re.search(time_pattern, message.lower())
        
        # Extract what to remind about
        about_pattern = r'remind\s+(?:me\s+)?(?:to\s+|about\s+)?(.*?)(?:\b(?:today|tomorrow|in|at)\b|$)'
        about_match = re.search(about_pattern, message.lower())
        
        if time_match and about_match:
            time_str = time_match.group(1)
            about = about_match.group(1).strip()
            
            # Convert time string to actual time
            remind_time = self._parse_reminder_time(time_str)
            
            reminder = {
                'about': about,
                'time': remind_time.isoformat(),
                'created': datetime.now().isoformat(),
                'completed': False
            }
            
            self.reminders.append(reminder)
            self._save_config()
            
            return f"I'll remind you to {about} {time_str}."
        else:
            return "I couldn't understand what you want to be reminded about or when. Could you please be more specific? For example: 'Remind me to call the client tomorrow at 10am.'"
    
    def _handle_calendar_query(self, message: str) -> str:
        """Handle calendar query requests"""
        # Extract date information
        date_pattern = r'\b(today|tomorrow|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        date_match = re.search(date_pattern, message.lower())
        
        if date_match:
            date_str = date_match.group(1)
            
            # Get appointments for the specified date
            if self.calendar_service:
                events = self._get_google_calendar_events(date_str)
                if events:
                    events_str = "\n".join([f"- {e['summary']} at {e['start_time']}" for e in events])
                    return f"Here's your schedule for {date_str}:\n{events_str}"
                else:
                    return f"You don't have any appointments scheduled for {date_str}."
            else:
                # Filter local appointments
                matching_appointments = self._filter_appointments_by_date(date_str)
                if matching_appointments:
                    appts_str = "\n".join([f"- {a['title']} at {a['time']}" for a in matching_appointments])
                    return f"Here's your schedule for {date_str}:\n{appts_str}"
                else:
                    return f"You don't have any appointments scheduled for {date_str}."
        else:
            # Show today's schedule by default
            return self._handle_calendar_query("What's on my calendar today?")
    
    def _parse_reminder_time(self, time_str: str) -> datetime:
        """Parse a time string into a datetime object"""
        now = datetime.now()
        
        if time_str.lower() == 'today':
            # Default to end of day
            return datetime(now.year, now.month, now.day, 17, 0)
        elif time_str.lower() == 'tomorrow':
            # Default to 9am tomorrow
            tomorrow = now + timedelta(days=1)
            return datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0)
        elif time_str.lower().startswith('in '):
            # Parse "in X minutes/hours/days"
            parts = time_str.lower().split()
            if len(parts) >= 3:
                amount = int(parts[1])
                unit = parts[2].rstrip('s')
                
                if unit == 'minute':
                    return now + timedelta(minutes=amount)
                elif unit == 'hour':
                    return now + timedelta(hours=amount)
                elif unit == 'day':
                    return now + timedelta(days=amount)
        elif time_str.lower().startswith('at '):
            # Parse "at X:XX am/pm"
            time_part = time_str[3:].strip()
            try:
                if ':' in time_part:
                    hour, minute = time_part.split(':')
                    hour = int(hour)
                    
                    # Handle am/pm
                    if 'pm' in minute.lower() and hour < 12:
                        hour += 12
                    elif 'am' in minute.lower() and hour == 12:
                        hour = 0
                        
                    minute = int(minute.rstrip('apmAPM').strip())
                    return datetime(now.year, now.month, now.day, hour, minute)
                else:
                    # Just hour provided
                    hour = int(time_part.rstrip('apmAPM').strip())
                    if 'pm' in time_part.lower() and hour < 12:
                        hour += 12
                    elif 'am' in time_part.lower() and hour == 12:
                        hour = 0
                        
                    return datetime(now.year, now.month, now.day, hour, 0)
            except ValueError:
                pass
                
        # Default to an hour from now if parsing fails
        return now + timedelta(hours=1)
    
    def _filter_appointments_by_date(self, date_str: str) -> List[Dict[str, Any]]:
        """Filter appointments by date string"""
        matching = []
        now = datetime.now()
        
        for appointment in self.appointments:
            appt_date = appointment['date'].lower()
            
            if date_str.lower() == 'today' and appt_date in ['today', now.strftime('%m/%d/%Y'), now.strftime('%m-%d-%Y')]:
                matching.append(appointment)
            elif date_str.lower() == 'tomorrow':
                tomorrow = now + timedelta(days=1)
                if appt_date in ['tomorrow', tomorrow.strftime('%m/%d/%Y'), tomorrow.strftime('%m-%d-%Y')]:
                    matching.append(appointment)
            elif date_str.lower() == appt_date:
                matching.append(appointment)
                
        return matching
    
    def _add_to_google_calendar(self, appointment: Dict[str, Any]) -> bool:
        """Add an appointment to Google Calendar"""
        if not self.calendar_service:
            return False
            
        try:
            # Parse date and time
            date_str = appointment['date']
            time_str = appointment['time']
            
            # Convert to datetime
            now = datetime.now()
            start_time = now
            end_time = now + timedelta(hours=1)
            
            # Very basic parsing - would need to be more robust in production
            if date_str.lower() == 'today':
                date_part = now.strftime('%Y-%m-%d')
            elif date_str.lower() == 'tomorrow':
                tomorrow = now + timedelta(days=1)
                date_part = tomorrow.strftime('%Y-%m-%d')
            else:
                # Try to parse m/d/y or m-d-y format
                try:
                    if '/' in date_str:
                        parts = date_str.split('/')
                    else:
                        parts = date_str.split('-')
                        
                    if len(parts) == 3:
                        month, day, year = parts
                    else:
                        month, day = parts
                        year = str(now.year)
                        
                    # Handle 2-digit year
                    if len(year) == 2:
                        year = '20' + year
                        
                    date_part = f"{year}-{int(month):02d}-{int(day):02d}"
                except:
                    # Fallback to today if parsing fails
                    date_part = now.strftime('%Y-%m-%d')
            
            # Parse time
            if ':' in time_str:
                hour, minute = time_str.split(':')
                hour = int(hour)
                
                # Handle am/pm
                if 'pm' in minute.lower() and hour < 12:
                    hour += 12
                elif 'am' in minute.lower() and hour == 12:
                    hour = 0
                    
                minute = int(minute.rstrip('apmAPM').strip())
            else:
                # Just hour provided
                hour = int(time_str.rstrip('apmAPM').strip())
                if 'pm' in time_str.lower() and hour < 12:
                    hour += 12
                elif 'am' in time_str.lower() and hour == 12:
                    hour = 0
                    
                minute = 0
                
            # Create start and end times
            start_time_str = f"{date_part}T{hour:02d}:{minute:02d}:00"
            end_time_str = f"{date_part}T{(hour + 1):02d}:{minute:02d}:00"
            
            # Create event
            event = {
                'summary': appointment['title'],
                'start': {
                    'dateTime': start_time_str,
                    'timeZone': 'America/New_York',  # Should be configurable
                },
                'end': {
                    'dateTime': end_time_str,
                    'timeZone': 'America/New_York',  # Should be configurable
                },
            }
            
            event = self.calendar_service.events().insert(
                calendarId=self.config.get("google_calendar_id", "primary"),
                body=event).execute()
                
            return True
        except Exception as e:
            print(f"Failed to add event to Google Calendar: {str(e)}")
            return False
    
    def _get_google_calendar_events(self, date_str: str) -> List[Dict[str, Any]]:
        """Get events from Google Calendar for a specified date"""
        if not self.calendar_service:
            return []
            
        try:
            # Parse date
            now = datetime.now()
            
            if date_str.lower() == 'today':
                start_date = datetime(now.year, now.month, now.day, 0, 0, 0)
                end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
            elif date_str.lower() == 'tomorrow':
                tomorrow = now + timedelta(days=1)
                start_date = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
                end_date = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 59, 59)
            elif date_str.lower() == 'this week':
                # Start of current week (Monday)
                start_date = now - timedelta(days=now.weekday())
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                # End of current week (Sunday)
                end_date = start_date + timedelta(days=6)
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            elif date_str.lower() == 'next week':
                # Start of next week (next Monday)
                start_date = now + timedelta(days=7 - now.weekday())
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                # End of next week (next Sunday)
                end_date = start_date + timedelta(days=6)
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            else:
                # Try to parse day of week
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                if date_str.lower() in days:
                    target_day = days.index(date_str.lower())
                    current_day = now.weekday()
                    days_ahead = (target_day - current_day) % 7
                    if days_ahead == 0:  # If today is the target day
                        if now.hour >= 12:  # If it's past noon, we likely mean next week
                            days_ahead = 7
                            
                    target_date = now + timedelta(days=days_ahead)
                    start_date = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
                    end_date = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
                else:
                    # Default to today if parsing fails
                    start_date = datetime(now.year, now.month, now.day, 0, 0, 0)
                    end_date = datetime(now.year, now.month, now.day, 23, 59, 59)
            
            # Format timestamps for Google Calendar API
            time_min = start_date.isoformat() + 'Z'  # 'Z' indicates UTC time
            time_max = end_date.isoformat() + 'Z'
            
            # Query Google Calendar
            events_result = self.calendar_service.events().list(
                calendarId=self.config.get("google_calendar_id", "primary"),
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime').execute()
                
            events = events_result.get('items', [])
            
            # Format results
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                # Parse start time for display
                if 'T' in start:
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    start_time = start_dt.strftime("%I:%M %p")  # Format as 11:30 AM
                else:
                    start_time = "All Day"
                    
                formatted_events.append({
                    'summary': event.get('summary', 'Untitled Event'),
                    'start_time': start_time,
                    'id': event['id']
                })
                
            return formatted_events
        except Exception as e:
            print(f"Failed to get events from Google Calendar: {str(e)}")
            return []
    
    def check_due_reminders(self) -> List[Dict[str, Any]]:
        """Check for reminders that are due and mark them as completed"""
        now = datetime.now()
        due_reminders = []
        
        for reminder in self.reminders:
            if not reminder['completed']:
                reminder_time = datetime.fromisoformat(reminder['time'])
                if reminder_time <= now:
                    due_reminders.append(reminder)
                    reminder['completed'] = True
        
        if due_reminders:
            self._save_config()
            
        return due_reminders
    
    def register_agent(self, agent_name: str, agent_role: str) -> str:
        """Register a new agent in the system"""
        if agent_name in self.agent_registry:
            return f"{agent_name} is already registered."
            
        self.agent_registry[agent_name] = {
            'role': agent_role,
            'registered': datetime.now().isoformat()
        }
        
        self._save_config()
        return f"Welcome to Dunder Mifflin, {agent_name}! I've added you to the directory."
    
    def get_agent_registry(self) -> Dict[str, Any]:
        """Get the current agent registry"""
        return self.agent_registry
    
    def get_upcoming_appointments(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get appointments for the next X days"""
        if self.calendar_service:
            # Use Google Calendar
            now = datetime.now()
            future = now + timedelta(days=days)
            
            time_min = now.isoformat() + 'Z'
            time_max = future.isoformat() + 'Z'
            
            try:
                events_result = self.calendar_service.events().list(
                    calendarId=self.config.get("google_calendar_id", "primary"),
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy='startTime').execute()
                    
                events = events_result.get('items', [])
                
                # Format results
                formatted_events = []
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    
                    # Parse start time for display
                    if 'T' in start:
                        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                        date_str = start_dt.strftime("%A, %B %d")
                        time_str = start_dt.strftime("%I:%M %p")
                    else:
                        start_date = datetime.fromisoformat(start)
                        date_str = start_date.strftime("%A, %B %d")
                        time_str = "All Day"
                        
                    formatted_events.append({
                        'title': event.get('summary', 'Untitled Event'),
                        'date': date_str,
                        'time': time_str,
                        'id': event['id']
                    })
                    
                return formatted_events
            except Exception as e:
                print(f"Failed to get events from Google Calendar: {str(e)}")
                return []
        else:
            # Use local appointments
            return self.appointments
    
    def run_reminder_check_loop(self, interval_seconds: int = 60) -> None:
        """Run a background loop to check for reminders (should be run in a separate thread)"""
        import time
        import threading
        
        def reminder_loop():
            while True:
                due_reminders = self.check_due_reminders()
                for reminder in due_reminders:
                    print(f"REMINDER: {reminder['about']}")
                    # In a real implementation, this would trigger notifications
                
                time.sleep(interval_seconds)
        
        reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()
        
        return reminder_thread


# Example usage
if __name__ == "__main__":
    pam = PamBot()
    
    # Test responses
    print(pam.respond("Remind me to call the e-renters insurance tomorrow @9:30AM"))
    print(pam.respond("Remind me that tomorrow at 1:30PM I have my annual review meeting with Jim Borg"))
    print(pam.respond("What's on my calendar today?"))
    
    # Register some agents
    print(pam.register_agent("Dwight Schrute", "Assistant to the Regional Manager"))
    print(pam.register_agent("Jim Halpert", "Sales"))
    
    # Print agent registry
    print("Agent Registry:", pam.get_agent_registry())
    
    # Start the reminder check loop in the background
    pam.run_reminder_check_loop()
    
    # In a real application, you'd have a proper event loop or web server here
    print("Pam Bot is running! Press Ctrl+C to exit.")
    try:
        while True:
            user_input = input("> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            print(pam.respond(user_input, {'user': 'Console User'}))
    except KeyboardInterrupt:
        print("\nGoodbye!")