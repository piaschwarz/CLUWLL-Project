import java.util.Scanner;
import java.io.*;


public class FrequencyListIntoJson {

	public static void main(String[] args) throws IOException {
		
		Scanner sc = new Scanner(new File("frequency_list_LemmaPosFreq.txt"));
		
		FileWriter fw = new FileWriter("frequency_list_LemmaPosFreq_json.json");
		
		//write the start of the json file 
		fw.write("[" + "\n");
		
		while(sc.hasNextLine())
		{
			String line = sc.nextLine();
			String[] arr = line.split("\t");
			String lemma = arr[0];
			String pos = arr[1];
			String freq = arr[2];
			
			fw.write("    "+ "{" + "\n" + "        " + "\"lemma\": "+"\""+lemma+"\","+ "\n");
			fw.write("        " + "\"pos\": "+"\""+pos+"\","+ "\n");
			fw.write("        " + "\"frequency\": "+"\""+freq+"\""+ "\n");

			fw.write("    "+ ""
					+ "}," + "\n");

		}
		fw.write("]");
		
		sc.close();
		fw.close();
	}

}
