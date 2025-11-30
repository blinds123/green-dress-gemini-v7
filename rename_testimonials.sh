#!/bin/bash

cd "/Users/nelsonchan/Downloads/secretjeans TEMPLATE SMALL copy 2/images/testimonials"

counter=1
for file in Generated\ Image*.webp; do
    if [ -f "$file" ]; then
        newname="testimonial-$(printf "%02d" $counter).webp"
        mv "$file" "$newname"
        echo "Renamed: $file -> $newname"
        counter=$((counter + 1))
    fi
done

echo "Total files renamed: $((counter - 1))"
