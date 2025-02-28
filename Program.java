
import java.util.Scanner;
public class Program {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    List list = new List();

    int op;
    do {
      showMenu();
      op = sc.nextInt();

      switch (op) {
        case 1: {
          System.out.println("Digite o valor a ser inserido no início da lista: ");
          Double value = sc.nextDouble();
          list.addIni(value);
          break;
        }
        case 2: {
          System.out.println("Digite o valor a ser inserido no final da lista: ");
          Double value = sc.nextDouble();
          list.addFim(value);
          break;
        }
        case 3: {
          System.out.println(list.toString());
          break;
        }
        case 4: {
          System.out.println("Lista invertida: " + list.inverterLista().toString());
          break;
        }
        case 5: {
          System.out.println("Programa Encerrado!");
          break;
        }
        default: {
          System.out.println("Opção inválida");
        }
      }
    } while (op != 5);
    sc.close();
  }



  public static void showMenu() {
    System.out.println("1 - Inserir no início da lista");
    System.out.println("2 - Inserir no final da lista");
    System.out.println("3 - Percorrer a lista");
    System.out.println("4 - Inverter ");
    System.out.println("5 - Sair");
  }

}
