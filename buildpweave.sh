pweave -s epython -f texminted $1.Pnw
pdflatex -shell-escape $1.tex
