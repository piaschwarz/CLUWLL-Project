import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletContext;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


public class UpdateLearnerTableServlet extends HttpServlet {
	
	
	private static final long serialVersionUID = 1L;
	private static String USER = "marta";
	private static String PASS = "colewe";
	
	private String username;
	private String lemmas;
	private String poses;
	private String difficulty;
	
	

	private void setAccessControlHeaders(HttpServletResponse resp) {
	    resp.setHeader("Access-Control-Allow-Origin", "*");
	    resp.setHeader("Access-Control-Allow-Methods", "GET");
	}
	
	
	/**
     * handles HTTP POST request. Example: http://localhost:8080/ServletCLUWLL/loginServlet?username=pia
     * @throws ServletException 
     */
	 public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException
	 {
		 setAccessControlHeaders(response);
		 
		//check if the user data is in the request (before the first round of vocab practice)
	    	if (request.getParameter("username") != null)
	    	{
	    		
	    		username = request.getParameter("username");
	    		lemmas = request.getParameter("lemma");
	    		poses = request.getParameter("pos");
	    		difficulty = request.getParameter("difficulty");



	    		
	    		
	    		
	    		
	    	} 
	    	
	    	
	    	response.setCharacterEncoding("UTF-8");		
	  		response.setContentType("text/html");
	  		PrintWriter out = new PrintWriter(new OutputStreamWriter(response.getOutputStream(), "UTF8"));
	  		out.println("<html><body>");
	  		
	  		out.println("<p>username is: ");
	  		out.println(username);
	  		out.println("</p>");
	  		
	  		out.println("<p>lemma is: ");
	  		out.println(lemmas);
	  		out.println("</p>");
	  		
	  		out.println("<p>pos is: ");
	  		out.println(poses);
	  		out.println("</p>");
	  		
	  		out.println("<p>difficulty is: ");
	  		out.println(difficulty);
	  		out.println("</p>");
	  		
	  		
	  		
	  		
	  		String[] lemmasArray = lemmas.split(","); //split the lemmas in the url
	  		String[] posArray = poses.split(",");//same with pos
	  		
	  		
	  		
	  		for (int i=0; i<lemmasArray.length; i++)
	  		{
	  			String lemma = lemmasArray[i];
	  			String pos = posArray[i];
	  			
	  			out.println("<p>single lemma is: ");
		  		out.println(lemma);
		  		out.println("</p>");
		  		out.println("<p>single pos is: ");
		  		out.println(pos);
		  		out.println("</p>");
		  		
	  		
	  		
	  		try {
				// Register JDBC driver
				Class.forName("com.mysql.cj.jdbc.Driver");
	    		
				String DB_URL = "jdbc:mysql://localhost/cluwll?serverTimezone=UTC";
	    		
	    		Properties info = new Properties();
	    		info.put( "user", USER );
	    		info.put( "password", PASS );
	    		info.put( "characterEncoding", "utf8" );
	    		
	    		Connection conn = DriverManager.getConnection(DB_URL, info);
	    		Statement stmt = conn.createStatement();
	    	
	    		
	    		stmt.executeQuery("USE cluwll;");
	    		
	    		// check what resultSet is returned for this query:
	    		String sqlStatement = "SELECT * from " + username + " where lemma = '" + lemma + "' AND pos = '" + pos + "';";
	    		ResultSet rs = stmt.executeQuery(sqlStatement);
	    		
	    		
	    		
	    		
	    		
	    		
	    		if(rs.isBeforeFirst()) 
	    		{ //if true: a record with pos = pos and lemma = lemma already exists
	    			//just update the record's difficulty as this can change
	    			
	    			
	    			stmt.executeUpdate("UPDATE " + username + 
	    					" SET difficulty = '" + difficulty + "' WHERE lemma = '" + lemma + "' AND pos = '" + pos + "';");
	    			
	    			
	    		} 
	    		else 
	    		{ //else: insert a new record
	    			
	    			
	    			
	    			stmt.executeUpdate("INSERT INTO " + username + " (lemma, pos, difficulty) VALUES ('" + lemma + "', '" + pos + "', '" + difficulty + "');");
	    		
	    			
	    		}
	    		
	    		
	    		conn.close();
	    	    
			
			} catch (SQLException e){
				e.printStackTrace();
			} catch (Exception ex) {
		        Logger lgr = Logger.getLogger(LoginServlet.class.getName());
		        lgr.log(Level.SEVERE, ex.getMessage(), ex);
			}
	  		
	  		
	  		}//end of for loop of lemmasArray
			
	        out.println("</body></html>");
			out.close();
	    	
	 }
	
	
	
	
	
	
	

}










