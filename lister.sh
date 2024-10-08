#!/bin/bash

cat <(jq .versions version_manifest_v2.json) <(jq .versions experimental_versions.json) | jq -s 'add.[].id' | tr -d '"' >version_list.txt
grep -P "(?!(?!^15w14a$)(^\d\dw\d\d[a-z]$)|(^\d.\d\d?((\.\d)\d?)?((-pre|-rc| Pre-Release )\d\d?)?$))(?!(^[abc]\d\.\d\d?(\.\d\d?)?(_\d\d?)?[a-z]?(_\d\d)?$)|(^((inf)|(rd))-\d+$))(?!^$)^.*" version_list.txt > special_versions.txt
grep -P "(?!^15w14a$)(^\d\dw\d\d[a-z]$)|(^\d.\d\d?((\.\d)\d?)?((-pre|-rc| Pre-Release )\d\d?)?$)(?!^$)" version_list.txt > normal_versions.txt
grep -P "(^[abc]\d\.\d\d?(\.\d\d?)?(_\d\d?)?[a-z]?(_\d\d)?$)|(^((inf)|(rd))-\d+$)" version_list.txt > old_versions.txt
