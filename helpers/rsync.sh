#!/bin/bash

# Usage: upload.sh --soft/hard --upload/download <local path> <remote path> [<substring in your pod id>]
# soft sync: only sync new files or existing files, won't delete any files from destination location even if they don't exist in source location
# hard sync: sync up files and delete all files that doesn't exist in source location

K8S_NAMESPACE='training-coreai'
# CLUSTER='prod-ltx1-k8s-2'
CLUSTER='prod-lva1-k8s-2'

if [ -z "$KRSYNC_STARTED" ]; then
    export KRSYNC_STARTED=true

    # Retrieve the pod id
    pod_id=$(
      kubectl -n $K8S_NAMESPACE --cluster $CLUSTER get pods -o=json | \
      jq -r --arg target "$5" --arg user "$(whoami)" '.items[] | select(.metadata.annotations["iddecorator.grid.li.username"] == $user and (.metadata.name | contains($target))) | {name: .metadata.name, creationTimestamp: .metadata.creationTimestamp}' | \
      jq -sr 'sort_by(.creationTimestamp) | .[-1].name'
    )
    if [ "$pod_id" = "null" ]; then
      echo -e "\033[0;31mNo pod found. Please check if your pod is running.\033[0m"
      exit 1
    fi
    echo -e "\033[0;34mUsing pod: $pod_id\033[0m"

    # Determine if this this is an upload or download operation
    if [ "$2" = "--upload" ]; then
        echo -e "\033[0;32mStart uploading ...\033[0m"
        src_dir=$3
        dst_dir="$pod_id:$4"
    elif [ "$2" = "--download" ]; then
        echo -e "\033[0;32mStart downloading ...\033[0m"
        src_dir="$pod_id:$4"
        dst_dir=$3
    else
        echo -e "\033[0;31mInvalid argument. Please use --upload or --download as the second argument.\033[0m"
        exit 1
    fi

    # Determine if this is a soft or hard sync and execute the rsync command
    if [ "$1" = "--hard" ]; then
        echo -n -e "\033[0;33mHard sync: all files that don't exist in source location will be deleted from destination location. Are you sure? [y/N]: \033[0m"
        read -r response
        response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
        if [ "$response" != "y" ] && [ "$response" != "yes" ]; then
            echo -e "\033[0;31mAborted.\033[0m"
            exit 1
        fi

        echo -e "\033[0;32mHard sync with pod $pod_id ...\033[0m"
        exec rsync -avz --filter=':- .gitignore' --delete --blocking-io --rsh "$0" -a "$src_dir" "$dst_dir"
    elif [ "$1" = "--soft" ]; then
        echo -e "\033[0;32mSoft sync with pod $pod_id ...\033[0m"
        exec rsync -avz --filter=':- .gitignore' --blocking-io --rsh "$0" -a "$src_dir" "$dst_dir"
    else
        echo -e "\033[0;31mInvalid argument. Please use --soft or --hard as the first argument.\033[0m"
        exit 1
    fi
fi

# Running as --rsh
kubectl -n $K8S_NAMESPACE --cluster $CLUSTER exec -i "$1" -- "${@:2}"
unset KRSYNC_STARTED
