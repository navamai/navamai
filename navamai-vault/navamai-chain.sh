# Save this script as `navamai-chain.sh` and make it executable with `chmod +x navamai-chain.sh`

# Initial prompt passed as the first argument
response=$(navamai ask "$1")

# Loop through the rest of the arguments
shift  # Shift the arguments to skip the first one
while [[ $# -gt 0 ]]; do
    prompt="$1"
    response=$(navamai ask "$(echo $prompt | sed "s/{}/$response/")")
    shift
done

# Output the final response
echo "$response"