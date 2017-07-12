package Entities;

import java.util.Random;
import eduni.simjava.*;

public class Source extends Sim_entity {
	private Sim_port in, in1, out, out1;
	private double delay;
	private Random numGen;
	private int ClientID;

	public Source(String name, double delay) {
		super(name);
		this.delay = delay;
		numGen = new Random();
		ClientID = 1;
		
		// Port for receiving new events
		in = new Sim_port("In");
		// Port for receiving events from Server
		in1 = new Sim_port("In1");
		// Port for creating new events
		out = new Sim_port("Out");
		// Port for sending events to Server
		out1 = new Sim_port("Out1");
		add_port(in);
		add_port(in1);
		add_port(out);
		add_port(out1);
	}

	public void body() {
		boolean simulationStart = true;
		
		while (Sim_system.running()) {
			if (simulationStart) {
				//First client of type 1
				sim_schedule(out, 0.0, 1, "Client " + ClientID++);
				//First client of type 2
				sim_schedule(out, 0.0, 2, "Client " + ClientID++);
				
				simulationStart = false;
			}
			
			Sim_event e = new Sim_event();
			sim_get_next(e);
			sim_process(delay);
			sim_completed(e);
			
			if (e.get_tag() == 1) {
				sim_schedule(out, numGen.nextInt(10) + 1, 1, "Client " + ClientID++);
				sim_schedule(out1, 0.0, 1, e.get_data());				
            } 
			else if (e.get_tag() == 2) {
				sim_schedule(out, numGen.nextInt(5) + 1, 2, "Client " + ClientID++);
				sim_schedule(out1, 0.0, 2, e.get_data());
            }
			else {
				sim_schedule(out1, 0.0, 3);
			}
		}
	}
}
