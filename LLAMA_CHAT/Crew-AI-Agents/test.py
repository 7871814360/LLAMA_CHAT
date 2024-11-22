from crewai import Crew, Process, Agent, Task
from sentence_transformers import SentenceTransformer
import ollama  # Import the Ollama library

# Initialize your embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define a function to get embeddings
def get_embeddings(text):
    return embedding_model.encode(text).tolist()

# Define the content writer agent
class CustomContentWriter(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def execute_task(self, task, context=None, tools=None):
        # Get the topic from the task description
        topic = task.description
        embeddings = get_embeddings(topic)  # Generate embeddings (if needed)

        # Use Ollama to generate content based on the topic
        generated_content = generate_with_ollama(topic)

        return generated_content

def generate_with_ollama(topic):
    # Prompt for Ollama
    prompt = f"Write a child-friendly paragraph about {topic}."
    
    # Call Ollama to generate content (adapt this to your setup)
    response = ollama.chat(prompt)  # Adjust based on your Ollama setup
    return response['message']  # Adjust based on how Ollama returns the response

# Define the research task
content_writer = CustomContentWriter(
    role='Blog Writer',
    goal='Generate a paragraph about {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner."
    ),
)

write_task = Task(
    description="Simplify the content to easy to learn by children.",
    expected_output='Key points based on the {topic}.',
    agent=content_writer,
)

# Form the tech-focused crew with enhanced configurations
crew = Crew(
    agents=[content_writer],
    tasks=[write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Start the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'Artificial Intelligence'})
print(result)
