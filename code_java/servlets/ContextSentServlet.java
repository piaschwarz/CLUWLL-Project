import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.json.JSONArray;
import org.json.JSONObject;


import javax.servlet.*;
import javax.servlet.http.*;



public class ContextSentServlet extends HttpServlet {

	private static final long serialVersionUID = 1L;
	private static String USER = "marta";
	private static String PASS = "colewe";
	private Connection conn;
	
	private void setAccessControlHeaders(HttpServletResponse resp) {
	    resp.setHeader("Access-Control-Allow-Origin", "*");
	    resp.setHeader("Access-Control-Allow-Methods", "GET");
	}
			
	public void doGet(HttpServletRequest request, HttpServletResponse response)	throws ServletException, IOException {
		setAccessControlHeaders(response);
		
		response.setCharacterEncoding("UTF-8");		
		response.setContentType("text/plain");
		PrintWriter out = new PrintWriter(new OutputStreamWriter(response.getOutputStream(), "UTF8"));
				
		String lemma = request.getParameter("lemma");
        
        
        
      	
			
		try {
			// Register JDBC driver
			Class.forName("com.mysql.cj.jdbc.Driver");
	    	String DB_URL = "jdbc:mysql://localhost/cluwll?serverTimezone=UTC";
	    	
	    	Properties info = new Properties();
	    	info.put( "user", USER );
	    	info.put( "password", PASS );
	    	info.put( "characterEncoding", "utf8" );
	    	
	    	Connection conn = DriverManager.getConnection(DB_URL, info);
	    	
	    	
	    	Statement stmt1 = conn.createStatement();
	    	
	    	
	    	
			ResultSet rs = stmt1.executeQuery("SELECT* FROM static WHERE lemma='"+lemma+"';");
			
			
			
	    	
	    	
	        
	       
	    	
	        JSONArray ja = new JSONArray();  
	        
	    	while (rs.next()) {
	    		
	    		String lemmaCS = rs.getString("lemma");
	    		String posCS = rs.getString("pos");

	    		String sent1ita = rs.getString("sent1ita");
		   		String sent2ita = rs.getString("sent2ita");
		   		String sent3ita = rs.getString("sent3ita");
		   		String sent1deu = rs.getString("sent1deu");
		   		String sent2deu = rs.getString("sent2deu");
		   		String sent3deu = rs.getString("sent3deu");
		   		String stringmatch1ita = rs.getString("stringmatch1ita");
		   		String stringmatch2ita = rs.getString("stringmatch2ita");
		   		String stringmatch3ita = rs.getString("stringmatch3ita");
		   		String stringmatch1deu = rs.getString("stringmatch1deu");
		   		String stringmatch2deu = rs.getString("stringmatch2deu");
		   		String stringmatch3deu = rs.getString("stringmatch3deu");		   		
		   		
		   		JSONObject jo = new JSONObject();
		   		jo.put("lemmaCS", lemmaCS);
		   		jo.put("posCS", posCS);
		   		jo.put("sent1ita",sent1ita);
		   		jo.put("sent2ita",sent2ita);
		   		jo.put("sent3ita",sent3ita);
		   		jo.put("sent1deu",sent1deu);
		   		jo.put("sent2deu",sent2deu);
		   		jo.put("sent3deu",sent3deu);
		   		jo.put("stringmatch1ita",stringmatch1ita);
		   		jo.put("stringmatch2ita",stringmatch2ita);
		   		jo.put("stringmatch3ita",stringmatch3ita);
		   		jo.put("stringmatch1deu",stringmatch1deu);
		   		jo.put("stringmatch2deu",stringmatch2deu);
		   		jo.put("stringmatch3deu",stringmatch3deu);
		   		
		   		
		   		//generate blanked sentences for Italian
		   		String sent1itablanked = sent1ita.replaceAll(stringmatch1ita, "_____");
		   		String sent2itablanked = sent2ita.replaceAll(stringmatch2ita, "_____");
		   		String sent3itablanked = sent3ita.replaceAll(stringmatch3ita, "_____");
		   		
		   		
		   		//generate blanked sentences for German
		   		//split the target words and replace all of them with blanks
		   		String[] stringmatch1deuItems = stringmatch1deu.split(" ");
		   		for (String item: stringmatch1deuItems) {
		   			sent1deu = sent1deu.replaceAll(item, "_____");
		   		}
		   		String sent1deublanked = sent1deu;
		   		
		   		
		   		//split the target words and replace all of them with blanks
		   		String[] stringmatch2deuItems = stringmatch2deu.split(" ");
		   		for (String item: stringmatch2deuItems) {
		   			
		   			sent2deu = sent2deu.replaceAll(item, "_____");
		   		}
		   		String sent2deublanked = sent2deu;
		   		
		   		
		   		//split the target words and replace all of them with blanks
		   		String[] stringmatch3deuItems = stringmatch3deu.split(" ");
		   		for (String item: stringmatch3deuItems) {
		   			sent3deu = sent3deu.replaceAll(item, "_____");
		   		}
		   		String sent3deublanked = sent3deu;
		   		
		   		
		   		jo.put("sent1itablanked",sent1itablanked);
		   		jo.put("sent2itablanked",sent2itablanked);
		   		jo.put("sent3itablanked",sent3itablanked);
		   		jo.put("sent1deublanked",sent1deublanked);
		   		jo.put("sent2deublanked",sent2deublanked);
		   		jo.put("sent3deublanked",sent3deublanked);
		   		
		   		ja.put(jo);
		   		
		   		
		   		
		   		
		   		
		   		
		   		
		   		
		        
	    	}
	    	
	   		//print out json object
	        out.print(ja);
	    	
	    	conn.close();
			
		} catch (SQLException e){
			e.printStackTrace();
		} catch (Exception ex) {
		    Logger lgr = Logger.getLogger(Random.class.getName());
		    lgr.log(Level.SEVERE, ex.getMessage(), ex);
		}
		
		out.close();
		
	}
	
	
	
	
	

}
