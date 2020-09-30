// class to find out which words on my lemmas list with context sentences were not found in the paisa corpus

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;

public class FrequencyStillNotFound {

	public static void main(String[] args) throws FileNotFoundException {
		
		
		//for each word on my lemmas list
		//if it is in the frequency_found file, then continue, if not, print it out
		
		File lemmas = new File("lemmas_list_with_context_sentences.txt");
		
		File freq_found = new File("found_frequencies.txt");
		

		//for each word on my lemmas list
		//if it is in the frequency_found file, then continue, if not, print it out
		
		Scanner sc_1 = new Scanner (lemmas);
		while (sc_1.hasNextLine())
		{
			String lemma = sc_1.nextLine();
			
			Scanner sc_2 = new Scanner (freq_found);
			
			boolean found = false;
			
			while (sc_2.hasNextLine())
			{
				String [] arr = sc_2.nextLine().split("\t");
				String lemma_with_freq = arr[0];
				
				if (lemma.equals(lemma_with_freq))
				{
					found = true;
				}
				
				
				
				
			}
			
			if (found==false)
			{
				System.out.println(lemma);
			}
			
			
		sc_2.close();	
		}
		
	sc_1.close();	
	}

}
