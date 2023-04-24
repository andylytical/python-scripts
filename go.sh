DEBUG=1
REGISTRY=ghcr.io
OWNER=andylytical
REPO=python-scripts


function latest_tag {
  [[ "$DEBUG" -eq 1 ]] && set -x
	# Replace <OWNER>, <REPO>, and <IMAGE> with the appropriate values for your container image.
  IMAGE=${REPO}
  URL="https://${REGISTRY}/v2/${OWNER}/${REPO}/${IMAGE}/tags/list"
	# local response=$(curl --silent "$URL")
	curl --silent "$URL"

	# Get the most recent tag by sorting the tags in reverse order and selecting the first one.
	# local latest_tag=$(echo "$response" | jq -r '.tags | sort -r | .[0]')
	# echo "$response" | jq -r '.tags | sort -r'

	# echo "$latest_tag"
}


[[ "$DEBUG" -eq 1 ]] && set -x

tag=$(latest_tag)
exit 1

docker run -it --pull always \
--mount type=bind,src=$HOME,dst=/home \
-e JIRA_SERVER=jira.ncsa.illinois.edu \
-e JIRA_PROJECT=SVCPLAN \
--entrypoint "/bin/bash" \
$REGISTRY/$REPO:$tag

