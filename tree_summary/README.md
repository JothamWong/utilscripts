# Tree Summary

Simple Ollama wrapper + tree util that also summarizes what each file does
with respect to the entire project.

Logging is performed at the moment, but the output is intended to be piped from stdout
as you would any other unix utility.

## Notes/Possible improvements?

At the moment, the Ollama model could take awhile. A smaller model is pretty
useless, and a larger model takes a really long time. Improvement to streaming the
output could be made.

Perhaps a better approach would be to summarize each directory first, and then
pass that summary as the context to the contents of the file?