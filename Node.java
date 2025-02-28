
public class Node {

	private Double value; //Atributo valor
	private Node next;    //Aponta para o próximo nó, que também é do tipo Node
	private Node previous; //Aponta para o nó anterior

	public Double getValue() {
		return value;
	}

	public void setValue(Double value) {
		this.value = value;
	}

	public Node getNext() {
		return next;
	}

	public void setNext(Node next) {
		this.next = next;
	}

	public Node getPrevious() {
		return previous;
	}

	public void setPrevious(Node previous) {
		this.previous = previous;
	}
}
