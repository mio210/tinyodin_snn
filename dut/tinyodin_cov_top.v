module tinyodin_cov_top (
    input  wire       clk,
    input  wire       rst,
    input  wire       sck,
    input  wire       mosi,
    input  wire       aerin_req,
    input  wire [9:0] aerin_addr,
    input  wire       aerout_ack,
    output wire       miso,
    output wire       aerin_ack,
    output wire [7:0] aerout_addr,
    output wire       aerout_req,
    output wire       sched_full,
    output wire [3:0] cov_ctrl_state,
    output wire [5:0] cov_spi_cnt,
    output wire [1:0] cov_opcode,
    output wire       cov_prog_event,
    output wire       cov_read_event,
    output wire       cov_gate_activity,
    output wire       cov_open_loop,
    output wire       cov_aer_source,
    output wire [7:0] cov_max_neur,
    output reg        cov_sq_reset_release,
    output reg        cov_sq_spi_program,
    output reg        cov_sq_aer_handshake,
    output reg        cov_sq_spi_then_aer,
    output reg        cov_sq_req_hold
);
    tinyODIN #(.N(256), .M(8)) dut (
        .CLK(clk), .RST(rst), .SCK(sck), .MOSI(mosi), .MISO(miso),
        .AERIN_ADDR(aerin_addr), .AERIN_REQ(aerin_req), .AERIN_ACK(aerin_ack),
        .AEROUT_ADDR(aerout_addr), .AEROUT_REQ(aerout_req),
        .AEROUT_ACK(aerout_ack), .SCHED_FULL(sched_full)
    );

    assign cov_ctrl_state    = dut.controller_0.state;
    assign cov_spi_cnt       = dut.spi_slave_0.spi_cnt;
    assign cov_opcode        = dut.CTRL_OP_CODE;
    assign cov_prog_event    = dut.CTRL_PROG_EVENT;
    assign cov_read_event    = dut.CTRL_READBACK_EVENT;
    assign cov_gate_activity = dut.SPI_GATE_ACTIVITY;
    assign cov_open_loop     = dut.SPI_OPEN_LOOP;
    assign cov_aer_source    = dut.SPI_AER_SRC_CTRL_nNEUR;
    assign cov_max_neur      = dut.SPI_MAX_NEUR;

    reg prev_rst;
    reg saw_spi_program;
    reg [2:0] req_run;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            prev_rst             <= 1'b1;
            saw_spi_program      <= 1'b0;
            req_run              <= 3'd0;
            cov_sq_reset_release <= 1'b0;
            cov_sq_spi_program   <= 1'b0;
            cov_sq_aer_handshake <= 1'b0;
            cov_sq_spi_then_aer  <= 1'b0;
            cov_sq_req_hold      <= 1'b0;
        end else begin
            cov_sq_reset_release <= prev_rst;
            prev_rst             <= 1'b0;
            cov_sq_spi_program   <= cov_prog_event;
            cov_sq_aer_handshake <= aerin_req && aerin_ack;
            cov_sq_spi_then_aer  <= saw_spi_program && aerin_ack;
            cov_sq_req_hold      <= aerin_req && (req_run >= 3);
            if (cov_prog_event) saw_spi_program <= 1'b1;
            if (!aerin_req) req_run <= 3'd0;
            else if (req_run != 3'd7) req_run <= req_run + 3'd1;
        end
    end
endmodule
