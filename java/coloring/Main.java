import java.util.*;
import java.io.*;
public class Main {
 

public static PrintWriter pw=new PrintWriter(System.out);
public static void solve() throws IOException{

	for(int i=1;i<=8;i++) graph[i]=new Vector<>();
	graph[1].add(3); graph[3].add(1);graph[1].add(2); graph[2].add(1);graph[2].add(3); graph[3].add(2);graph[2].add(4); graph[4].add(2);
	graph[3].add(5); graph[5].add(3);graph[4].add(5); graph[5].add(4);graph[4].add(6); graph[6].add(4);graph[4].add(7); graph[7].add(4);
	graph[5].add(6); graph[6].add(5);graph[6].add(7); graph[7].add(6);graph[7].add(8); graph[8].add(7);graph[6].add(8); graph[8].add(6);
    dfs(1);
    pw.println(mx);
    for(int i=1;i<=8;i++) pw.print(color[i]+" ");
	pw.close();
}
static int available[]=new int[9];
static int color[]=new int[9];
static boolean vis[]=new boolean[9];
static Vector<Integer> graph[]=new Vector[9];
static int mx=0;
static void dfs(int v){
	vis[v]=true;


	for(int u : graph[v]){
		available[color[u]]=1;
	}

	for(int i=1;i<=8;i++){
		if(available[i]==0){
			color[v]=i;
			mx=Math.max(i,mx);
			available[i]=1;
			break;
		}
	}
	for(int u : graph[v]) available[color[u]]=0;
	for(int u : graph[v]){
		if(!vis[u]) dfs(u);
	}
}
public static void main(String[] args) throws IOException  {
          new Thread(null ,new Runnable(){
            public void run(){
                try{
                    solve();
                } catch(Exception e){
                    e.printStackTrace();
                }
            }
        },"1",1<<26).start();
	 
}

}
