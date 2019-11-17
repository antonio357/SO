#include <stdio.h>
#define quantumTime 1
#define true 1
#define false 0


// Estrutura do processo com os atributos necessários
struct Process {
    int processID;
    int processingTime; // Tempo que o processo leva ocupando CPU
    int waitTime; // Tempo que o processo espera até poder ocupar a CPU
    int turnAroundTime; // Tempo que o processo leva até poder terminar sua tarefa (processingTime + waitTime)
    int arrivalTime; // simula o tempo em que o processo entrou no escalonador
    int leftTimeToExecute; // contabiliza todo o tempo que o processo executou
} Process;

// Calcula o waitTime para cada processo
struct Process *calculateWaitTime(struct Process queue[], int size) {
    for (int i = 1; i < size; i++) {
        queue[i].waitTime = queue[i - 1].processingTime + queue[i - 1].waitTime;
    }
    return queue;
}

// Calcula quanto tempo o processo leva desde a espera até o fim da execução
struct Process *calculateTurnAround(struct Process queue[], int size) {
    for (int i = 0; i < size; i++) {
        queue[i].turnAroundTime = queue[i].processingTime + queue[i].waitTime;
    }
    return queue;
}

// Retorna o tempo médio de espera para cada processo
void averageWaitingTime(struct Process queue[], int size) {
    float average = 0;
    int count = 0;
    for (int i = 0; i < size; i++) {
        average += queue[i].waitTime;
        count++;
    }
    average = average / count;
    printf ("Average Waiting Time: %f\n", average);
}

// Troca itens em um array
void swap(struct Process *a, struct Process *b) {
    struct Process t = *a;
    a = b;
    b = &t;
}

// Função auxiliar para o quick sort
int partition(struct Process queue[], int low, int high) {
    int pivot = queue[high].processingTime;
    int i = low - 1;
    for (int j = low; j <= high - 1; j++) {
        if (queue[j].processingTime <= pivot) {
            i++;
            swap (&queue[i], &queue[j]);
        }
    }
    swap (&queue[i + 1], &queue[high]);
    return (i + 1);
}

// Quick Sort
void quickSort(struct Process queue[], int low, int high) {
    if (low < high) {
        int pi = partition (queue, low, high);
        quickSort (queue, low, pi - 1);
        quickSort (queue, pi + 1, high);
    }
}

// FCFS
void firstComeFirstServed(struct Process queue[], int size) {
    queue = calculateWaitTime (queue, size);
    queue = calculateTurnAround (queue, size);
    averageWaitingTime (queue, size);
}

// Job mais curto primeiro
void shortestJobNext(struct Process queue[], int size) {
    quickSort (queue, 0, size - 1);
    queue = calculateWaitTime (queue, size);
    queue = calculateTurnAround (queue, size);
    averageWaitingTime (queue, size);
}

// conferi se o processo já pode ser executado, já que o programa agora simula tempo de chegada "arrivalTime"
int processHasArrived(struct Process process, int actual_time) {
    if (actual_time >= process.arrivalTime) 
        return true;
    return false;
}

// realiza os ajustes no processo atual que esta sendo executado pela cpu 
int executeProcess(struct Process* process) {
    int dif = process->leftTimeToExecute - quantumTime;
    if (dif >= 0) { // processo executou todo o quantumTime que a ele foi dado
        process->leftTimeToExecute -= quantumTime;
        return 0;
    }
    else { // processo terminou de executar e sobrou tempo do quantumTime cedido 
        process->leftTimeToExecute = 0;
        return dif * -1;
    }
}

// ajusta o tempo esperado de todos os processos que estão no escalonador
void caculateWaitTimeRoundRobin(struct Process queue[], int size, int actual_time, int executionTime, int actualRunningProcessID) {
    for (int i = 0; i < size; i++) {
        if (queue[i].processID != actualRunningProcessID && processHasArrived(queue[i], actual_time) == true) 
            queue[i].waitTime += executionTime;
    }
    
}

// verifica se todos os processos já concluiram
int stillHaveProcess(struct Process queue[], int size) {
    for (int i = 0; i < size; i++){
        if (queue[i].leftTimeToExecute > 0) return true; 
    }
    return false;
}

// Round Robin
void roundRobin(struct Process queue[], int size) {
    int actual_time = 0; // registra quanto tempo se passou desde a cpu começou a rodar o primeiro processo
    int remainingTime; 
    int executionTime;

    while (true) {
        executionTime = 0;

        for (int i = 0; i < size; i++) {
            if (processHasArrived(queue[i], actual_time) == true && queue[i].leftTimeToExecute > 0) {
                remainingTime = executeProcess(&(queue[i])); // tempo restante do quantumTime cedido ao processo 
                executionTime = quantumTime - remainingTime; // tempo que o processo passou executando
                actual_time += executionTime;
                
                caculateWaitTimeRoundRobin(queue, size, actual_time, executionTime, queue[i].processID);
            }
        }

        /* é necessario caso ocorra de os processos no escalonador todos terminarem de executar 
        e ainda ter processos que não atingiram seu arrivaltime */
        actual_time += quantumTime; // faz o actual time funcionar como relógio

        if (executionTime == 0 && stillHaveProcess(queue, size) == false) break; 
    }

    calculateTurnAround(queue, size);
    averageWaitingTime(queue, size);
}

int main() {
    // Array de processos com seus IDs e tempos de processamento
    struct Process queue[] = {{1, 6, 0, 0, 5, 6},
                              {2, 8, 0, 0, 2, 8},
                              {3, 7, 0, 0, 3, 7},
                              {4, 3, 0, 0, 0, 3},
                              {5, 1, 0, 0, 4, 1}};

    // Calculando o número de itens em um array
    int size = sizeof (queue) / sizeof (struct Process);

    /*
     * Descomente o algoritmo que você quer usar e comente os outros
     * Você não deve usar vários ao mesmo tempo pois os resultados serão indeterminados     *
     */

    // firstComeFirstServed(queue, size);
    // shortestJobNext(queue, size); 
    roundRobin(queue, size);
    printf ("ProcessID | Processing Time | Wait Time | Turnaround Time\n");
    for (int i = 0; i < size; i++) {
        printf ("%d \t\t % d \t\t % d \t\t % d \n", queue[i].processID, queue[i].processingTime, queue[i].waitTime, queue[i].turnAroundTime);
    }
    return 0;
}