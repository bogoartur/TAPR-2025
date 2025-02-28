package Stacks;
import java.util.Scanner;
public class Program {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    Stack stack = new Stack();

    int op;
    do {
      showMenu();
      op = sc.nextInt();

      switch (op) {
        case 1: {
          System.out.println("Digite o valor a ser inserido na pilha: ");
          int value = sc.nextInt();
          stack.addElement(value);
          break;
        }
        case 2: {
            System.out.println(stack.toString());
            break;
        }
        case 3: {
          stack.removeElement();
          System.out.println("Aqui está a lista novamente" + stack.toString());
          break;
        }
        case 4: {
          System.out.println("Programa Encerrado!");
          break;
        }
        default: {
          System.out.println("Opção inválida");
        }
      }
    } while (op != 4);
    sc.close();
  }



  public static void showMenu() {
    System.out.println("1 - Inserir na pilha");
    System.out.println("2 - Percorrer a pilha");
    System.out.println("3 - Remover da pilha");
    System.out.println("4 - Sair");

  }

}
