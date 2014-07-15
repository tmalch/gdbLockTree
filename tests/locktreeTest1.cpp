#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// http://en.wikipedia.org/wiki/POSIX_Threads 
#define NUM_THREADS     2
 
pthread_mutex_t l1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t l2 = PTHREAD_MUTEX_INITIALIZER;
 
void *task_code(void *argument)
{
   int tid;
   tid = *((int *) argument);
   
   for(int loop=0;loop<10;loop++){
		 if(tid == 1){
		 	pthread_mutex_lock(&l1);
		 	pthread_mutex_lock(&l2);
			printf("Hello World! It's me, thread %d!\n", tid);
			pthread_yield();
		  pthread_mutex_unlock(&l2);
		  pthread_mutex_unlock(&l1);
		 }else{
		 	pthread_mutex_lock(&l2);
		 	pthread_mutex_lock(&l1);
			printf("Hello World! It's me, thread %d!\n", tid);
			pthread_yield();
		  pthread_mutex_unlock(&l1);   
		  pthread_mutex_unlock(&l2);
		 }
 	 }
   return NULL;
}




int main(void)
{
   pthread_t threads[NUM_THREADS];
   int thread_args[NUM_THREADS];
   int rc, i;
 
   // create all threads one by one
   for (i=0; i<NUM_THREADS; ++i) {
      thread_args[i] = i;
      printf("In main: creating thread %d\n", i);
      rc = pthread_create(&threads[i], NULL, task_code, (void *) &thread_args[i]);
      assert(0 == rc);
   }
 
   // wait for each thread to complete
   for (i=0; i<NUM_THREADS; ++i) {
      // block until thread i completes
      rc = pthread_join(threads[i], NULL);
      printf("In main: thread %d is complete\n", i);
      assert(0 == rc);
   }
 
   printf("In main: All threads completed successfully\n");
   exit(EXIT_SUCCESS);
}
