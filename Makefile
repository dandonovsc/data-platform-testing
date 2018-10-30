clean:
	find . -name "*.pyc" -exec rm -f {} \;

package:
	zip -r app app



