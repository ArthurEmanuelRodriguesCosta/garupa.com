import java.io.PrintWriter;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Random;

import eduni.simjava.Sim_entity;
import eduni.simjava.Sim_event;
import eduni.simjava.Sim_port;
import eduni.simjava.Sim_system;

public class Simulator2 extends Sim_entity {

	private static Random random = new Random();

	private Queue<Integer> queue1 = new LinkedList<>();
	private Queue<Integer> queue2 = new LinkedList<>();
	private Integer current = null;

	private PrintWriter writer;

	public Simulator2(String name, PrintWriter writer) {
		super(name);
		this.writer = writer;

		Sim_port in = new Sim_port("In");
		Sim_port out = new Sim_port("Out");

		add_port(in);
		add_port(out);
	}

	private void log(String type) {
		writer.println("Tipo de evento: " + type + ", Momento do evento: " + Sim_system.clock());
		writer.println("Elementos na Fila 1: " + queue1);
		writer.println("Elementos na Fila 2: " + queue2);
		writer.println("Elemento no serviço: " + current);
	}

	@Override
	public void body() {
		boolean init = true;
		int count = 0;

		while (Sim_system.running()) {

			if (init) {
				sim_schedule("Out", 0, 1);
				sim_schedule("Out", 0, 2);

				init = false;
			}

			Sim_event e = new Sim_event();
			sim_get_next(e);

			if (e.get_tag() == 1) {
				sim_schedule("Out", randomDelay(1, 10), 1);
				Integer id = ++count;

				if (current != null)
					queue1.add(id);

				else {
					current = id;
					sim_schedule("Out", randomDelay(3, 7), 3);
				}

				log("Chegada");
			}

			if (e.get_tag() == 2) {
				sim_schedule("Out", randomDelay(1, 5), 2);
				Integer id = ++count;

				if (current != null)
					queue2.add(id);

				else {
					current = id;
					sim_schedule("Out", randomDelay(3, 7), 3);
				}

				log("Chegada");
			}

			if (e.get_tag() == 3) {
				current = queue1.isEmpty()? queue2.poll() : queue1.poll();
				sim_schedule("Out", randomDelay(3, 7), 3);

				log("Saída");
			}

			sim_completed(e);
		}
	}

	private double randomDelay(double min, double max) {
		return min + (max-min) * random.nextDouble();
	}

	public static void simulate(int duration) {
		PrintWriter writer = null;

		try {
			writer = new PrintWriter("sim_output", "utf-8");
		} catch (Exception e) {}

		Sim_system.initialise();
		new Simulator2("Simulator", writer);
		Sim_system.link_ports("Simulator", "Out", "Simulator", "In");

		Sim_system.set_termination_condition(Sim_system.TIME_ELAPSED, duration, false);
		Sim_system.run();

		writer.close();
	}

	public static void main(String[] args) {
		simulate(100);
	}
}
