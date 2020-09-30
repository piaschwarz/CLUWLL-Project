
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.Arrays; 
import java.util.Collections;
import java.io.File;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.File;  // Import the File class
import java.io.IOException;  // Import the IOException class to handle errors

public class LevenshteinDistance {
	
	
	/**
     * <p>Find the Levenshtein distance between two Strings.</p>
     *
     * <p>A higher score indicates a greater distance.</p>
     *
     * <p>The previous implementation of the Levenshtein distance algorithm
     * was from <a href="https://web.archive.org/web/20120526085419/http://www.merriampark.com/ldjava.htm">
     * https://web.archive.org/web/20120526085419/http://www.merriampark.com/ldjava.htm</a></p>
     *
     * <p>This implementation only need one single-dimensional arrays of length s.length() + 1</p>
     *
     * <pre>
     * unlimitedCompare(null, *)             = IllegalArgumentException
     * unlimitedCompare(*, null)             = IllegalArgumentException
     * unlimitedCompare("","")               = 0
     * unlimitedCompare("","a")              = 1
     * unlimitedCompare("aaapppp", "")       = 7
     * unlimitedCompare("frog", "fog")       = 1
     * unlimitedCompare("fly", "ant")        = 3
     * unlimitedCompare("elephant", "hippo") = 7
     * unlimitedCompare("hippo", "elephant") = 7
     * unlimitedCompare("hippo", "zzzzzzzz") = 8
     * unlimitedCompare("hello", "hallo")    = 1
     * </pre>
     *
     * @param left the first String, must not be null
     * @param right the second String, must not be null
     * @return result distance, or -1
     * @throws IllegalArgumentException if either String input {@code null}
     */
    private static int unlimitedCompare(CharSequence left, CharSequence right) {
        if (left == null || right == null) {
            throw new IllegalArgumentException("Strings must not be null");
        }

        /*
           This implementation use two variable to record the previous cost counts,
           So this implementation use less memory than previous impl.
         */

        int n = left.length(); // length of left
        int m = right.length(); // length of right

        if (n == 0) {
            return m;
        } else if (m == 0) {
            return n;
        }

        if (n > m) {
            // swap the input strings to consume less memory
            final CharSequence tmp = left;
            left = right;
            right = tmp;
            n = m;
            m = right.length();
        }

        int[] p = new int[n + 1];

        // indexes into strings left and right
        int i; // iterates through left
        int j; // iterates through right
        int upper_left;
        int upper;

        char rightJ; // jth character of right
        int cost; // cost

        for (i = 0; i <= n; i++) {
            p[i] = i;
        }

        for (j = 1; j <= m; j++) {
            upper_left = p[0];
            rightJ = right.charAt(j - 1);
            p[0] = j;

            for (i = 1; i <= n; i++) {
                upper = p[i];
                cost = left.charAt(i - 1) == rightJ ? 0 : 1;
                // minimum of cell to the left+1, to the top+1, diagonally left and up +cost
                p[i] = Math.min(Math.min(p[i - 1] + 1, p[i] + 1), upper_left + cost);
                upper_left = upper;
            }
        }

        return p[n];
    }

	
	public static void main(String[] args) throws IOException 
    { 
		LevenshteinDistance Lev = new LevenshteinDistance();
		
		File file = new File("levenshtein_full.txt");
		Scanner scanner = new Scanner(file);
		
		//String str_1 = "occorrere";
        //String sentence = "Per tutto questo ci occorrono personalità convincenti che rappresentino l'Europa e che siano rispettate da tutte le parti in conflitto in Medio Oriente.";
        //String[] sentence_arr = sentence.split(" ");
        
		
		FileWriter file_output = new FileWriter ("output_levenshtein.tsv");
		
        while (scanner.hasNextLine())
        {
        	String line = scanner.nextLine();
        	//System.out.println(line);
        	
        	String[] columns = line.split("\t");
        	
        	
        	
        	String lemma = columns[0];
        	System.out.println(lemma);
        	file_output.write(lemma + "\t");
        

        	//create array with the 3 italian sentences
        	String[] sentences = {columns[2],columns[5],columns[8]};
        	
        	for (String sentence : sentences)
        	{
        		ArrayList<Integer> arr_values = new ArrayList<Integer>();
                HashMap<Integer, String> hmap = new HashMap<Integer, String>();
                
                
              //for each italian sentence, create an array with each word
              sentence = sentence.replaceAll("\\p{Punct}"," ");
              String [] words_arr = sentence.split(" ");
              
              for (String word : words_arr)
              {
            	  int value = Lev.unlimitedCompare(lemma, word);
            	  arr_values.add(value);
            	  hmap.put(value, word);
              }
              
              int min = Collections.min(arr_values);
              

              
              file_output.write(hmap.get(min) + "\t");
                
        	}
        	
        	
        	file_output.write("\n");
             
             
            
             
             


        	
        	
        }
        
        scanner.close();
        file_output.close();
        
        
    } 
}
