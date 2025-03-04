#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve PHI model..."
ollama pull phi
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid