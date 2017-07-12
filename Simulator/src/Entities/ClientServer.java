package Entities;

import java.util.LinkedList;
import java.util.Queue;
import java.util.Random;
import eduni.simjava.*;

public class ClientServer extends Sim_entity {
	private Sim_port in, out;
	private double delay;
	private String serverState;
	private Queue < String > queue1, queue2;
	private Random numGen;
	
	public ClientServer(String name, double delay) {
		super(name);
		this.delay = delay;
		serverState = "Empty";
		queue1 = new LinkedList < String >();
		queue2 = new LinkedList < String >();
		numGen = new Random();
		
		// Port for receiving events from the Scheduler
		in = new Sim_port("In");
		// Port for sending events to Scheduler
		out = new Sim_port("Out");
		add_port(in);
		add_port(out);
	}

	public void body() {
		while (Sim_system.running()) {
			Sim_event e = new Sim_event();
			sim_get_next(e);
			sim_process(delay);
			sim_completed(e);
			
			if (e.get_tag() == 1) {
				sim_trace(1, "Tipo de evento: Chegada, Momento do evento: " + Sim_system.clock());
				
				if (serverState.compareTo("Empty") != 0) queue1.add((String) e.get_data());
				else {
					serverState = (String) e.get_data();
					sim_schedule(out, numGen.nextInt(5) + 3, 3);
				}
			}
			else if (e.get_tag() == 2) {
				sim_trace(1, "Tipo de evento: Chegada, Momento do evento: " + Sim_system.clock());
				
				if (serverState.compareTo("Empty") != 0) queue2.add((String) e.get_data());
				else {
					serverState = (String) e.get_data();
					sim_schedule(out, numGen.nextInt(5) + 3, 3);
				}
			}
			else {
				sim_trace(1, "Tipo de evento: Saída, Momento do evento: " + Sim_system.clock());
				
				if (!queue1.isEmpty()) {
					serverState = queue1.poll();
					sim_schedule(out, numGen.nextInt(5) + 3, 3);
				}
				else if (!queue2.isEmpty()) {
					serverState = queue2.poll();
					sim_schedule(out, numGen.nextInt(5) + 3, 3);
				}
				else serverState = "Empty";
			}
			
			sim_trace(1, "Elementos na Fila 1: " + queue1.toString());
			sim_trace(1, "Elementos na Fila 2: " + queue2.toString());
			sim_trace(1, "Elemento no serviço: " + serverState);
			sim_trace(1, "");
		}
	}
}
