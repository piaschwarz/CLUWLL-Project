import java.util.Scanner;
import java.io.*;


public class FlashIntoJson {

	public static void main(String[] args) throws IOException
	{
		
		Scanner sc = new Scanner(new File("flashcardsa1a2_alphabetical.txt"));
		
		FileWriter fw = new FileWriter("flashcardsa1a2_alpha_json.json");
		fw.write("[" + "\n");

		while(sc.hasNextLine())
		{
			String line = sc.nextLine();
			String[] arr = line.split("\t");
			String lemma = arr[0];
			String senses = arr[1];
			
			fw.write("    "+ "{" + "\n" + "        " + "\"lemma\": "+"\""+lemma+"\","+ "\n");
			fw.write("        " + "\"senses\": "+"\""+senses+"\","+ "\n");
			fw.write("        " + "\"isClicked\": " + "\"false\""+"\n");
			fw.write("    "+ ""
					+ "}," + "\n");
		
			
		}
		fw.write("]");
		
		sc.close();
		fw.close();
	}
}
