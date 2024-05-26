package test.mvc;

import java.awt.Font;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.swing.JSpinner;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import mvc.Controller;
import mvc.Model;
import mvc.View;

public class TestMVCApp {

    private static final String OUTPUT_FILE = "data.csv";
    static final int NUMBER_OF_VIEWS = 100;
    static final int NUMBER_OF_SPINNER = NUMBER_OF_VIEWS;
    static final int DIVIDER = 4;

    public static void main(String[] args) throws IOException {
        long startTime = System.currentTimeMillis();

        // delete the target data file if the file exists
        Files.deleteIfExists(Path.of(OUTPUT_FILE));

        // create a new target data file
        Files.writeString(Path.of(OUTPUT_FILE),
                "iter,view_total,view_num,spin_total,spin_num,time,memory" + System.lineSeparator(),
                StandardCharsets.UTF_8, StandardOpenOption.CREATE);
        System.out.println("iter,view_total,view_num,spin_total,spin_num,time,memory");

        // perform performance measurement 12 times
        for (int i = 1; i <= 12; i++) {
            performMeasurement(i);
        }

        long endTime = System.currentTimeMillis();
        long totalTimeInMillis = endTime - startTime;
        double totalTimeInMinutes = totalTimeInMillis / 1000.0 / 60.0; // Convert milliseconds to minutes
        System.out.println("Total Time: " + totalTimeInMinutes + " minutes");
    }

    private static void performMeasurement(int iteration) throws IOException {

        // create number of views array. In this experiment, it consists of four
        // categories: 1, 25, 50, 75, 100.
        List<Integer> viewTotalList = new ArrayList<>();
        viewTotalList.add(1);
        for (int multiplier1 = 1; multiplier1 <= DIVIDER; multiplier1++) {
            int val = (int) (NUMBER_OF_VIEWS / DIVIDER * multiplier1);
            viewTotalList.add(val);
        }

        for (int viewTotal : viewTotalList) {

            // create number of spinner pairs array. In this experiment, it consists of four
            // categories: 1, 25, 50, 75, 100.
            List<Integer> spinnerTotalList = new ArrayList<>();
            spinnerTotalList.add(1);
            for (int multiplier2 = 1; multiplier2 <= DIVIDER; multiplier2++) {
                int val = (int) (NUMBER_OF_SPINNER / DIVIDER * multiplier2);
                spinnerTotalList.add(val);
            }

            List<View> viewList = new ArrayList<>();

            for (int spinnerTotal : spinnerTotalList) {

                // clear views created in the previous iteration
                // and also do garbage collection
                viewList.clear();
                System.gc();

                for (int viewNumber = 1; viewNumber <= viewTotal; viewNumber++) {
                    // create the view, model, and controller
                    Model model = new Model(String.valueOf(((NUMBER_OF_VIEWS * 10) + viewNumber)));
                    View view = new View();
                    view.setName(String.valueOf(viewNumber));
                    view.setTitle("View" + ((NUMBER_OF_VIEWS * 10) + viewNumber));
                    view.getContentPane().removeAll();
                    view.setDefaultCloseOperation(View.DISPOSE_ON_CLOSE);
                    viewList.add(view);

                    // set model and view relationship
                    model.setView(view);
                    Controller.getModels().put(model.getName(), model);

                    // create the input and output spinners.
                    // the number of spinners is as many as the order of the view.
                    // for example, if the current view is the 8th view, than the view contains
                    // 8 input spinners and 8 output spinners
                    for (int spinnerNumber = 0; spinnerNumber < spinnerTotal; spinnerNumber++) {

                        JSpinner inputSpinner = new JSpinner();
                        inputSpinner.setName("spinner" + ((viewTotal * 10) + spinnerNumber));
                        ((JSpinner.DefaultEditor) inputSpinner.getEditor()).getTextField().setColumns(3);
                        inputSpinner.setFont(new Font("Dialog", Font.BOLD, 32));
                        view.getContentPane().add(inputSpinner);

                        JSpinner outputSpinner = new JSpinner();
                        outputSpinner.setEnabled(false);
                        outputSpinner.setName("spinner" + ((viewTotal * 10) + spinnerNumber) + "b");
                        ((JSpinner.DefaultEditor) outputSpinner.getEditor()).getTextField().setColumns(3);
                        outputSpinner.setFont(new Font("Dialog", Font.BOLD, 32));
                        view.getContentPane().add(outputSpinner);

                        inputSpinner.addChangeListener(new ChangeListener() {
                            @Override
                            public void stateChanged(ChangeEvent e) {
                                int value = (int) inputSpinner.getValue();
                                Controller.handleChange(model.getName(), inputSpinner.getName(), value);
                            }
                        });
                    }

                    view.setVisible(true);
                }

                // Wait for a while to let the UI finish rendering
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                for (View view : viewList) {
                    view.dispose();
                }

                // Construct the output string and write to file
                String outputString = constructOutputString(iteration, viewTotal, spinnerTotal);
                if (viewTotal > 1 && spinnerTotal > 1) {
                    Files.writeString(Path.of(OUTPUT_FILE), outputString, StandardCharsets.UTF_8,
                            StandardOpenOption.APPEND);
                    System.out.print(outputString);
                }
            }
        }
    }

    private static String constructOutputString(int iteration, int viewTotal, int spinnerTotal) {
        StringBuilder output = new StringBuilder();
        for (int i = 0; i < spinnerTotal; i++) {
            output.append(String.format("%d,%d,%d,%d,%d,%d,%d%n", iteration, viewTotal, viewTotal, spinnerTotal, i,
                    System.currentTimeMillis(), Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()));
        }
        return output.toString();
    }
}
