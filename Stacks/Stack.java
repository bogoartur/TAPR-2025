package Stacks;
public class Stack {
    private Element top;
    private int totaldeElementos = 0;

    public void addElement(int value) {
        Element element = new Element();
        element.setValue(value);
        if (totaldeElementos == 0) {
            element.setAbove(null);
            element.setBelow(null);
            top = element;
            totaldeElementos += 1;
        } else {
            top.setAbove(element);
            element.setBelow(top);
            top = element;
            totaldeElementos += 1;
            
        }
    }

    public void removeElement() {
        if (totaldeElementos == 0) {
            System.out.println("Quer remover oq porra");
        } else {
            top = top.getBelow();
            totaldeElementos--;
        }
    }

    @Override
    public String toString() {
        StringBuffer sb = new StringBuffer();
        sb.append("[");
        Element p = top;
        while(p != null) {
            sb.append(p.getValue() + " ");
            p = p.getBelow();
        }
        sb.append("]");
        return sb.toString();
    }

}

