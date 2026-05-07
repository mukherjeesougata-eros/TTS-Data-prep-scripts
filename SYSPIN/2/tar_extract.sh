for f in *.tar.gz; do
    echo "Extracting $f"
    tar -xzf "$f" -C SYSPIN_extracted/
done
