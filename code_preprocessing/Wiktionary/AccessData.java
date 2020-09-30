package learnit.process_wiktionary;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;

import de.tudarmstadt.ukp.jwktl.JWKTL;
import de.tudarmstadt.ukp.jwktl.api.IQuotation;
import de.tudarmstadt.ukp.jwktl.api.IWikiString;
import de.tudarmstadt.ukp.jwktl.api.IWiktionaryEdition;
import de.tudarmstadt.ukp.jwktl.api.IWiktionaryEntry;
import de.tudarmstadt.ukp.jwktl.api.IWiktionarySense;
import de.tudarmstadt.ukp.jwktl.api.PartOfSpeech;
import de.tudarmstadt.ukp.jwktl.api.WiktionaryFormatter;
import de.tudarmstadt.ukp.jwktl.api.filter.WiktionaryEntryFilter;
import de.tudarmstadt.ukp.jwktl.api.util.GrammaticalGender;
import de.tudarmstadt.ukp.jwktl.api.util.ILanguage;
import de.tudarmstadt.ukp.jwktl.api.util.Language;

public class AccessData {
	private static String TARGET_DIRECTORY = "/Users/marta/cluwll/Project/wiktionary-data";
	
	public static void main(String[] args) {
		
		extractSenses("A1-B2_with_ids_for-extraction.tsv", "senses.tsv");
		
	}
	
	// for every word, find senses that correspond to word's part of speech; write all senses with their own ids in the file
	public static void extractSenses(String inputFile, String outputFile) {
		try {
			// open file to read words from
			BufferedReader reader = new BufferedReader(new FileReader(inputFile));
			// open file to write senses to
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
			
			// hash map for correspondence of parts of speech between Wikipedia and the book
			HashMap<String, String> pos_correspondence = new HashMap<String, String>();
			pos_correspondence.put("noun", "substantiv");
			pos_correspondence.put("adjective", "adjektiv");
			pos_correspondence.put("pronoun", "pronomen");
			pos_correspondence.put("adverb", "adverb");
			pos_correspondence.put("verb", "verb");
			pos_correspondence.put("preposition", "präposition");
			pos_correspondence.put("conjunction", "konjunktion");
			pos_correspondence.put("interjection", "interjektion");
			pos_correspondence.put("article", "artikel");
			pos_correspondence.put("personal_pronoun", "personalpronomen");
			pos_correspondence.put("interrogative_pronoun", "interrogativpronomen");
			pos_correspondence.put("demonstrative_pronoun", "demonstrativpronomen");
			pos_correspondence.put("possessive_pronoun", "possessivpronomen");
			pos_correspondence.put("indefinite_pronoun", "indefinitpronomen");
			pos_correspondence.put("idiom", "redewendung");
			
			// connect to the Wiktionary database
			File wiktionaryDirectory = new File(TARGET_DIRECTORY);
			IWiktionaryEdition wkt = JWKTL.openEdition(wiktionaryDirectory);
			
			// id for senses
			int sense_id = 1;
			
			
			
			String line;
			// for every line, extract word id, word itself and pos according to the book
			while ((line=reader.readLine()) != null) {
				String[] columns = line.split("\t");
				String word_id = columns[0].trim();
				String word = columns[1].trim();
				String pos_file = columns[2].trim();
				

				boolean ifHasSense = false;

				boolean ifHasEntry = false;
				// if part of speech is the same as in the book
				boolean ifPosSame = false;
				

				List<IWiktionaryEntry> entries = wkt.getEntriesForWord(word);
				for (IWiktionaryEntry entry : entries) {
					ILanguage language = entry.getWordLanguage();
					
					// check if language of entry is Italian
					if ((language != null) && (language.getName().equals("Italian"))) {
						
						ifHasEntry = true;
								
						// get part/parts of speech
						List<PartOfSpeech> poses = entry.getPartsOfSpeech();
						
						for (PartOfSpeech pos : poses) {
							pos = entry.getPartOfSpeech();
							
							if (pos != null) {
								String pos_wkt = pos.toString().toLowerCase();
								// check if part of speech of word and part of speech of entry is the same
								if (pos_correspondence.containsKey(pos_wkt) && pos_file.equalsIgnoreCase(pos_correspondence.get(pos_wkt))) {
									

									
									ifPosSame = true;
												
									// get senses
									for (IWiktionarySense sense : entry.getSenses()) {
										String sense_text = sense.getGloss().getPlainText();
										ifHasSense = true;
										writer.write(sense_id + "\t" + sense_text + "\t" + word_id + "\n");
										sense_id += 1;
									}
								}
							}
						}
					}
				}
				
				
			
			// close files
			writer.close();
			reader.close();
					
			// close the database connection
			wkt.close();
			
			
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
