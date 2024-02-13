module clk_buf(input A, output X);
assign X = A;
endmodule

(* blackbox *)
module break_comb_loop(input A, output X);
assign X = A;
endmodule
