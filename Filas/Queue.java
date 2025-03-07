package Filas;

public class Queue {
    private Element first;
    private Element front;
    private int totaldeElementos = 0;

    public void addElement(int value) {
        Element element = new Element();
        element.setValue(value);
        if (totaldeElementos == 0) {
            element.setBehind(null);
            first = element;
            front = first;
            totaldeElementos += 1;
        } else {
            front.setBehind(element);
            front = element;
            totaldeElementos += 1;
        }
    }

    public void removeElement() {
        if (totaldeElementos == 0) {
            System.out.println("Quer remover oq?");
        } else {
            first = first.getBehind();
            totaldeElementos--;
        }
    }

    @Override
    public String toString() {
        StringBuffer sb = new StringBuffer();
        sb.append("[");
        Element p = front;
        while(p != null) {
            sb.append(p.getValue() + " ");
            p = p.getBehind();
        }
        sb.append("]");
        return sb.toString();
    }

}
