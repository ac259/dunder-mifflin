```ansi
        ╔═════════════════════════════════════════════════════════════════════╗
        ║                                                                     ║
        ║  ██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗                 ║
        ║  ██╔══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗                ║
        ║  ██║  ██║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝                ║
        ║  ██║  ██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗                ║
        ║  ██████╔╝╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║                ║
        ║  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝                ║
        ║                                                                     ║
        ║  ███╗   ███╗██╗███████╗███████╗██╗     ██╗███╗   ██╗                ║
        ║  ████╗ ████║██║██╔════╝██╔════╝██║     ██║████╗  ██║                ║
        ║  ██╔████╔██║██║█████╗  █████╗  ██║     ██║██╔██╗ ██║                ║
        ║  ██║╚██╔╝██║██║██╔══╝  ██╔══╝  ██║     ██║██║╚██╗██║                ║
        ║  ██║ ╚═╝ ██║██║██║     ██║     ███████╗██║██║ ╚████║                ║
        ║  ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝                ║
        ║                                                                     ║
        ║  DUNDER MIFFLIN TERMINAL                                            ║
        ║  Unlimited paper in a paperless world                               ║
        ╚═════════════════════════════════════════════════════════════════════╝
```

Inspired by The Office, Dunder Mifflin AI is an agentic system designed to bring a mix of humor and efficiency to your everyday tasks. 
Whether it’s scheduling meetings (without double-booking like Michael Scott), managing emails (unlike Kevin’s famous chili disaster), or even delivering sarcastic but useful productivity insights à la Jim Halpert,
this AI assistant is here to help.

With a playful nod to Scranton’s most beloved paper company, this system doesn’t just get things done—it does them with the kind of quirky personality that makes work fun. 
Think of it as an AI Dwight Schrute: hyper-efficient, knowledgeable, and occasionally over-the-top, but ultimately making your life easier.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/ac259/dunder-mifflin
   ```

2. Install dependencies:
    ```python
    cd dunder-mifflin
    pip install -r requirements.txt
    ```
3. Run the system:
    ```python
    python main.py
    ```

## Running the CLI

```bash
python cli/dunder_cli.py
```

### Usage

```plaintext
/agents        # Show all available agents
/use jim       # Talk in Jim's voice
/use darryl    # Ask coding questions
/history       # View previous interactions
/exit          # Leave the office
```

Or just typing Natural Language

```plaintext
[PAM] > generate code for adding two numbers in python
```

### Example Interaction

```plaintext
[PAM] > generate code for adding two numbers in python

def add_numbers(x, y):
    """Adds two numbers."""
    return x + y

# Example
print(add_numbers(10, 5))  # Output: 15
```

## 🧪 Agent Roles

```plaintext
| Agent         | Role                                                           |
|---------------|----------------------------------------------------------------|
| **Pam**       | Orchestrates and routes user queries intelligently             |
| **SchruteBot**| Task manager, disciplinarian, Dwightisms included              |
| **JimsterAgent** | Mischief-maker. May put your request in Jell-O             |
| **DarrylAgent** | Code writer, debugger, warehouse genius                      |
```

## Documentation

For detailed information on the architecture, agents, and folder structure, please refer to our [documentation](docs).


## Contributing

We welcome contributions! Please see our [contributing guidelines](docs/CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
