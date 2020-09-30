import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
public class Frequency {
	
	public static void main(String[] args) throws FileNotFoundException {
		
		//read in file with lemmas and frequencies (written in a descending order accoridng to frequency rate)
		//for each word of the file with frequencies, go through file of lemmas for our app
		//if the word is contained in the second file, print it in another file in the format lemma \t frequency
		//if word is not found, print it to console
		
		File freq = new File("lemmas_frequencies_paisa.txt");
		File lemmas = new File("lemmas_list_with_context_sentences.txt");
		
		Scanner sc_1 = new Scanner (freq);
		
		
		while (sc_1.hasNextLine())
		{
			String line = sc_1.nextLine();
			String [] lemmaFreqArr = line.split("\t");
			String lemmaF = lemmaFreqArr[0];
			String frequency = lemmaFreqArr[1];
			
			Scanner sc_2 = new Scanner (lemmas);
			
			while (sc_2.hasNextLine())
			{
				String lemma = sc_2.nextLine();
				
				
				if (lemmaF.equals(lemma))
				{
					System.out.println(lemmaF + "-" + frequency);
				}
				
				
			}
			
			
			
		sc_2.close();	
		}
		
		sc_1.close();
		
		
		
	}

}
