package Filas;

public class Element {
    private int value;
    public int getValue() {
        return value;
    }
    public void setValue(int value) {
        this.value = value;
    }
    private Element behind;
    public Element getBehind() {
        return behind;
    }
    public void setBehind(Element behind) {
        this.behind = behind;
    }

}