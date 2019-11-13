synopsis.html: synopsis.md killya_er_model.png killya_relational_schema.png
	markdown synopsis.md > synopsis.html

synopsis.pdf: synopsis.md killya_er_model.png killya_relational_schema.png
	pandoc -o synopsis.pdf synopsis.md

dist: synopsis.md synopsis.html synopsis.pdf killya_er_model.png killya_relational_schema.png
	tar -czvf 111703013_assignment_4_miniproject_problem_erdiagram_schema.tar.gz synopsis.md synopsis.pdf synopsis.html killya_er_model.png killya_relational_schema.png

clean: 
	rm synopsis.pdf synopsis.html
