import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
// Import the FileWriter class
import java.io.*;
import java.util.Scanner;
import java.util.SortedSet;
import java.util.TreeSet;




public class FlashA1A2 {
	
	static HashMap<String, ArrayList<String>> Flash() throws IOException{
		
		Scanner sc_2= new Scanner(new File("a1a2ids.tsv"));
		
		HashMap flashcards = new HashMap<String, ArrayList<String>>();
		
		while(sc_2.hasNextLine()) //read through each line of a1a2ids and senses
		{
			String a1a2Line = sc_2.nextLine();
			String[] arra1a2 = a1a2Line.split("\t");
			String id = arra1a2[0];
			String lemma = arra1a2[1];
			String pos = arra1a2[2];
			String level = arra1a2[3];
			
			
			
			
			Scanner sc_1 = new Scanner(new File("senses.tsv"));	
			while (sc_1.hasNextLine()) 
			{
				String sensesLine = sc_1.nextLine();
				String[] arrsenses = sensesLine.split("\t");
				String sense = arrsenses[1];
				sense = sense + " ";
				String senseId= arrsenses[2];
				
				
				
				
				ArrayList<String> al = new ArrayList<String>();
				
				
				//if lemma id == sense id
					//if key(lemma) doesnt exist yet, add sense to arraylist, put a new key-value combination in the hashmap
					//if key exists already, add sense id to the arraylist and update the value at the lemma key
				if 	(id.equals(senseId))
				{
					if (flashcards.containsKey(lemma))
					{
						ArrayList<String> existing = (ArrayList<String>) flashcards.get(lemma);
						sense = "// " + sense;
						existing.add(sense);
						flashcards.replace(lemma, existing);
						
					}
					else
					{
						al.add(sense);
						flashcards.put(lemma, al);
					}
				}
				
			
			}
			
			

			
			
			
		sc_1.close();	
			
		}
		
		
		sc_2.close();
		
		
		
		FileWriter myWriter = new FileWriter("flashcardsa1a2_alphabetical.txt");
		
		SortedSet<String> keys = new TreeSet<String>(flashcards.keySet());
		for (String key : keys)
		//for (Object key : flashcards.keySet())
		{
			if (flashcards.containsKey(key))
			{
				myWriter.write(key + "\t");
				
				ArrayList<String> alSenses = (ArrayList<String>) flashcards.get(key);
				
				for (String sense : alSenses)
				{
					myWriter.write(sense);
				}
				myWriter.write("\n");
			}
		}
		
		myWriter.close();
		
		
		
		return flashcards;
		
		
		
}

	
	
	

public static void main(String[] args) throws IOException {
	
	Flash();
	System.out.println("ok");

}




}



