
public class List {

	private Node head;
	private Node tail;
	private Node lastNode;
	private Node previousNode;
	private int totalDeElementos = 0;
	
	public void addIni(Double value) {
		//1 - Inserir no início da lista
		
		Node node = new Node();
		node.setValue(value); 
		
		if (head == null) { //se nao tiver elemento, obta no inicio
			head = node; //head é o ultimo elemento
			tail = node;// tail é o primeiro elemento
			tail.setPrevious(null); //como nao tinha elementos, nao tem anterior, fica [1]
		} else {
			node.setNext(head); //transforma o head [1], no proximo falor do novo node
			head.setPrevious(node); //transforma o novo node no previous do head
			head = node;
		}
		totalDeElementos++;
	}

	public void addFim(Double value) {
		//2 - Inserir no final da lista
        if (totalDeElementos == 0) {
			addIni(value);
		} else {
			Node node = new Node();
			node.setValue(value);
			tail.setNext(node);

			node.setPrevious(tail);

			tail = node;

			totalDeElementos++;
			
		}
	}



	@Override
	public String toString() {    
		//5 - Percorrer a lista (Imprimir)
		//Aqui estamos utilizando a classe StringBuffer 
		//que é muito útil para otimizar a construção de Strings potencialmente grandes
		StringBuffer sb = new StringBuffer(); 
		sb.append("[");
		
		Node p = head;
		while (p != null) {
			sb.append(p.getValue() + " ");
			p = p.getNext();
		}
		
		sb.append("]");
		return sb.toString();
	}

	public String inverterLista() {
		StringBuffer sb = new StringBuffer(); 
		sb.append("[");
		
		Node p = tail;
		while (p != null) {
			sb.append(p.getValue() + " ");
			p = p.getPrevious();
		}
		sb.append("]");
		return sb.toString();


}
}