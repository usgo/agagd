## Include All Styles
## https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md
all

## Set Some Rules
rule 'MD026', punctuation: ',:;'

## General Markdown Exclusions

## First Line in file should be a top level header
## Breaks on Github Issue Templates
exclude_rule 'MD002'
exclude_rule 'MD041'

## Line Length
exclude_rule 'MD013'

## Bare URL
exclude_rule 'MD034'
