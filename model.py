from transformers import pipeline
import pandas as pd 
data = {}
# Use a pipeline as a high-level helper
pipe = pipeline("text-classification", model="Dc-4nderson/tone-classifier")
