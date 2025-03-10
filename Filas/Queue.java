package Filas;

public class Queue {
    private Element first;
    private Element rear;
    private int totaldeElementos = 0;

    public void addElement(int value) {
        Element element = new Element();
        element.setValue(value);
        element.setBehind(null);
        if (totaldeElementos == 0) {
            first = element;
            rear = first;
        } else {
            rear.setBehind(element);
            rear = element;
        }
        totaldeElementos += 1;
    }

    public void removeElement() {
        if (totaldeElementos == 0) {
            System.out.println("Quer remover oq?");
        } else {
            first = first.getBehind();
            totaldeElementos--;
        }
        if (totaldeElementos == 0) {
            rear = null;
        }
    }

    @Override
    public String toString() {
        StringBuffer sb = new StringBuffer();
        sb.append("[");
        Element p = first;
        while(p != null) {
            sb.append(p.getValue() + " ");
            p = p.getBehind();
        }
        sb.append("]");
        return sb.toString();
    }

}
