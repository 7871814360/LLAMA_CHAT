from crewai_tools import YoutubeChannelSearchTool
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")

# Initialize your tool with the API key if necessary
yt_tool = YoutubeChannelSearchTool(api_key=api_key, youtube_channel_handle='@krishnaik06')