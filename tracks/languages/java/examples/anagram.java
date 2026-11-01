import java.util.Arrays;
import java.util.Scanner;

public class anagram {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("Enter the first String: ");
        String first = in.nextLine();
        System.out.println("Enter the second String: ");
        String second = in.nextLine();

        if(checkIfStringsHaveSameLetters(first, second)){
            System.out.println("Both Strings are anagram.");
        }else{
            System.out.println("Current Strings are not anagram.");
        }
    }
    static boolean checkIfStringsHaveSameLetters(String firstString, String secondString){
        char []letters1 = firstString.toCharArray();
        char []letters2 = secondString.toCharArray();
        Arrays.sort(letters1);
        Arrays.sort(letters2);
        firstString = String.valueOf(letters1);
        secondString = String.valueOf(letters2);

        return firstString.equals(secondString);
    }
}
