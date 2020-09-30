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

public class AccessLearnerTableServlet extends HttpServlet{
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
	
		String username = request.getParameter("username");

		
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
	    	ResultSet rs = stmt.executeQuery("SELECT* FROM " + username + ";");
			
	    	
	    	JSONArray ja = new JSONArray();
	    	
	    	while (rs.next()) 
	    	{
	    		String lemma = rs.getString("lemma");
	    		String pos = rs.getString("pos");
	    		String difficulty = rs.getString("difficulty");
	    		
	    		
	    		JSONObject jo = new JSONObject();
		   		jo.put("lemma", lemma);
		   		jo.put("pos", pos);
		   		jo.put("difficulty", difficulty);
		   		
		   		ja.put(jo);


		   		


	    	}
	    	
	    	
	    	//print out json object
	        out.print(ja);
	    	
	    	conn.close();
	    	
	    	
	    	
		}//try
		
		catch (SQLException e){
			e.printStackTrace();
		} catch (Exception ex) {
		    Logger lgr = Logger.getLogger(Random.class.getName());
		    lgr.log(Level.SEVERE, ex.getMessage(), ex);
		}
		
		out.close();
		
		
		
		
	}	

}
