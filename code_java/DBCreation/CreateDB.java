package CreateDBCluwll.CreateDBCluwll;
import java.sql.*;
import java.util.Properties;

public class CreateDB {
	
	// Database credentials
		static final String USER = "marta";
		static final String PASSWORD = "colewe";
		

		// JDBC driver name and database URL
		static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
		static final String DB_URL = "jdbc:mysql://localhost/cluwll?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";


		public static void main(String[] args) {
			
			
			
			try 
			{
				// initialize data base driver
				Class.forName(JDBC_DRIVER);
				
				
				//connect to database
				
				Properties info = new Properties();
				info.put( "user", USER);
				info.put( "password", PASSWORD );
				info.put( "characterEncoding", "utf8" );
				Connection conn = DriverManager.getConnection(DB_URL, info);
				
				//create statement
				Statement stat = conn.createStatement();
				
				//execute query
				String insertion = "LOAD DATA LOCAL INFILE '/home/marta/eclipse-workspace/CreateDBCluwll/static_full_list_sorted_freq.tsv' INTO TABLE static;"; //insert the content of the corpus in the table
				stat.executeUpdate(insertion);
				
				
				conn.close();
				
				System.out.println("Insertion completed");
				
			}
			
			catch (Exception e)
			{
				e.printStackTrace();
			}
			
		}
}
