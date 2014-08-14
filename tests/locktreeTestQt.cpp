 #include <Qt/qmutex.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>
#define NUM_THREADS     2
 
QMutex l1;
QMutex l2;
QMutex l3;
void *task_code(void *argument)
{
   int tid;
   tid = *((int *) argument);

   for(int loop=0;loop<10;loop++){
		 l3.lock();
		 if(tid == 1){
		 	l1.lock();
		 	l2.lock();
			printf("Hello World! It's me, thread %d!\n", tid);
//			pthread_yield();
		  l2.unlock();
		  l1.unlock();
		 }else{
		 	l2.lock();
		 	l1.lock();
			printf("Hello World! It's me, thread %d!\n", tid);
//			pthread_yield();
		  l1.unlock();
		  l2.unlock();
		 }
		 l3.unlock();
 	 }
   return NULL;
}


//g++ -o qt.out -g locktreeTestQt.cpp -lpthread -lQtCore -I/usr/include/qt4/

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
