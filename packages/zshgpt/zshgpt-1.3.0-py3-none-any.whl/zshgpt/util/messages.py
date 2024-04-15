from openai.types.beta.thread_create_params import Message

raw_messages = [
    {'role': 'user', 'content': '# login to git with user.name=martha-nielsen user.email=martha.nielsen@gmail.com'},
    {
        'role': 'assistant',
        'content': '''git config --global user.name "martha-nielsen"
git config --global user.email "martha.nielsen@gmail.com"''',
    },
    {'role': 'user', 'content': '# what processes are hogging the most cpu?'},
    {'role': 'assistant', 'content': 'ps aux | sort -nrk 3,3 | head -n 10.'},
    {'role': 'user', 'content': '# add a hello world website to the index'},
    {
        'role': 'assistant',
        'content': "echo '<html><body><h1>Hello World!</h1></body></html>' > web-app/index.html",
    },
    {'role': 'user', 'content': '# open it with vi'},
    {'role': 'assistant', 'content': 'vi web-app/index.html'},
    {'role': 'user', 'content': '# How do I make a greek salad explained in 4 lines or less'},
    {
        'role': 'assistant',
        'content': """# To make a Greek salad, you will need:
# 1. Chop tomatoes, cucumbers, and red onions.
# 2. Add feta cheese, Kalamata olives, and fresh herbs like oregano.
# 3. Drizzle olive oil and lemon juice as dressing.
# 4. Toss everything together and serve.

# Enjoy your Greek salad!
""",
    },
    {'role': 'user', 'content': "# what's running on port 1018?"},
    {'role': 'assistant', 'content': 'lsof -i :1018'},
    {'role': 'user', 'content': '# kill process 1584'},
    {'role': 'assistant', 'content': 'kill -9 1584'},
    {'role': 'user', 'content': '# what other devices are on my network?'},
    {'role': 'assistant', 'content': 'arp -a'},
    {'role': 'user', 'content': '# how much storage is left?'},
    {'role': 'assistant', 'content': 'df -h'},
    {'role': 'user', 'content': '# Tell me a joke'},
    {
        'role': 'assistant',
        'content': """# Sure, here's a joke for you: Why did the tomato turn red?

# Because it saw the salad dressing!""",
    },
]

messages = [Message(role=message['role'], content=message['content']) for message in raw_messages]
_only_user_messages = [message for message in messages if message['role'] == 'user']
