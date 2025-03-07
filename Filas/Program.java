package Filas;
import java.util.Scanner;
public class Program {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    Queue queue = new Queue();

    int op;
    do {
      showMenu();
      op = sc.nextInt();

      switch (op) {
        case 1: {
          System.out.println("Digite o valor a ser inserido na fila: ");
          int value = sc.nextInt();
          queue.addElement(value);
          break;
        }
        case 2: {
            System.out.println("-----------");
            System.out.println(queue.toString());
            break;
        }
        case 3: {
          queue.removeElement();
          System.out.println("Aqui está a lista novamente" + "\n" + queue.toString());
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
    System.out.println("-----------------");
    System.out.println("1 - Inserir na fila");
    System.out.println("2 - Percorrer a fila");
    System.out.println("3 - Remover da fila");
    System.out.println("4 - Sair");

  }

}