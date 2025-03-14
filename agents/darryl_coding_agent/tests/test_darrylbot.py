import pytest 
import asyncio
from darryl_coding_agent.darryls_tech_warehouse import DarrylBot 

@pytest.mark.asyncio
async def test_generate_code():
    bot = DarrylBot()
    response = await bot.generate_code("print('Hello, World!')")
    assert response is not None  # Ensures function does not error

@pytest.mark.asyncio
async def test_debug_code():
    bot = DarrylBot()
    response = await bot.debug_code("x = 1\ny = x + z")
    assert response is not None  # Ensures function does not error

@pytest.mark.asyncio
async def test_optimize_code():
    bot = DarrylBot()
    response = await bot.optimize_code("for i in range(len(arr)): print(arr[i])")
    assert response is not None  # Ensures function does not error
