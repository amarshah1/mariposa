import os, random, subprocess
from utils.query_utils import Mutation, emit_mutant_query
from utils.system_utils import *
from base.defs import MARIPOSA

class MutCoreBuilder:
    def __init__(self, input_query, solver, output_query, timeout):
        log_check(os.path.exists(input_query), f"input query {input_query} does not exist")
        self.solver = solver

        name_hash = get_name_hash(input_query)

        self.input_query = input_query
        self.__gen_subdir = f"gen/{name_hash}/"
        self.lbl_query = f"gen/{name_hash}/lbl.smt2"
        self.lbl_mut_query = f"gen/{name_hash}/lbl.mut.smt2"
        self.core_log = f"gen/{name_hash}/z3-core.log"
        self.timeout = timeout
        self.output_query = output_query

        self.__create_label_query()

        for _ in range(60):
            remove_file(self.lbl_mut_query)
            remove_file(self.core_log)

            s = random.randint(0, 0xffffffffffffffff)
            emit_mutant_query(self.lbl_query, self.lbl_mut_query, 
                              Mutation.COMPOSE, s)

            with open(self.lbl_mut_query, "a") as f:
                f.write("(get-unsat-core)\n")

            success = self.__run_solver(seed=s)

            if success:
                log_info(f"successfully used mutant seed: {s}")
                self.__create_core_query(seed=s)
                self.clear_temp_files()
                return
            else:
                log_info(f"failed to use mutant seed: {s}")

        self.clear_temp_files()
        exit_with(f"failed to use mutants {self.solver} on {input_query}, no core log created")
        
    def clear_temp_files(self):
        remove_dir(self.__gen_subdir)

    def __create_label_query(self):
        if os.path.exists(self.lbl_query):
            # we do not expect labelled query to change ...
            log_info(f"{self.lbl_query} already exists")
            return

        subprocess.run([
            MARIPOSA,
            "-i", self.input_query,
            "-o", self.lbl_query, 
            "--action=label-core",
        ])

        # we do not expect labeling to fail
        if not os.path.exists(self.lbl_query):
            exit_with(f"failed to create {self.lbl_query}")

    def __run_solver(self, seed):
        cf = open(self.core_log, "w+")
        start = time.time()
        args = self.solver.get_basic_command(
            self.lbl_mut_query, self.timeout, seed)
        subprocess.run(args, stdout=cf)
        cf.close()
        elapsed = time.time() - start
        cf = open(self.core_log, "r")
        lines = cf.readlines()
        cf.close()
        log_info(f"elapsed: {elapsed} seconds")

        if len(lines) == 0 or "unsat\n" not in lines:
            os.remove(self.core_log)
            return False
        return True

    def __create_core_query(self, seed):
        remove_file(self.output_query)

        subprocess.run([
            MARIPOSA,
            "-i", self.lbl_query,
            "--action=reduce-core",
            f"--core-log-path={self.core_log}",
            f"-o", self.output_query,
        ])

        log_check(os.path.exists(self.output_query), f"failed to create core query {self.output_query}")

        with open(self.output_query, "a") as f:
            f.write(f'(set-info :comment seed_{seed})\n')
