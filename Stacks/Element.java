package Stacks;
public class Element {
    private int value;
    public int getValue() {
        return value;
    }
    public void setValue(int value) {
        this.value = value;
    }
    private Element below;
    public Element getBelow() {
        return below;
    }
    public void setBelow(Element below) {
        this.below = below;
    }

    private Element above;
    public Element getAbove() {
        return above;
    }
    public void setAbove(Element above) {
        this.above = above;
    }
}
