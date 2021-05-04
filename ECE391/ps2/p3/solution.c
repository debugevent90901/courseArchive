typedef struct martian_english_message_lock
{
    // The type of synchronization primitive you may use is {\fix spinlock\_t}.
    // You may add up to 3 elements to this struct.
    spinlock_t spinlock; // spin-lock used to lock the shared queue
    int num_eng;         // number of English messages in "translated message queues"
    int num_mar;         // number of Martian messages in "translated message queues"
} me_lock;

void melon_input(me_lock *lock, msg *message)
{
    unsigned long flag;
    while (1)
    {
        if (lock->num_mar < 4 && lock->num_eng == 0) // check validity of number of messages
        {
            spin_lock_irqsave(&(lock->spinlock), flag);  // if valid, get the lock
            if (lock->num_mar >= 4 || lock->num_eng > 0) // check again after getting the lock
            {
                spin_unlock_irqrestore(&(lock->spinlock), flag); // invalid: unlock
            }
            else
            {
                break;
            }
        }
    }
    // critical section
    translate_to_martian(message);
    lock->num_mar++;
    spin_unlock_irqstore(&(lock->spinlock), flag);
    return;
}

void martian_input(me_lock *lock, msg *message)
{
    unsigned long flag;
    while (1)
    {
        if (lock->num_eng < 10) // check validity of number of messages
        {
            spin_lock_irqsave(&(lock->spinlock), flag); // if valid, get the lock
            if (lock->num_eng >= 10)                    // check again after getting the lock
            {
                spin_unlock_irqrestore(&(lock->spinlock), flag); // invalid: unlock
            }
            else
            {
                break;
            }
        }
    }
    // critical section
    translate_to_english(message);
    lock->num_eng++;
    spin_unlock_irqstore(&(lock->spinlock), flag);
    return;
}

int melon_get_output(me_lock *lock, msg *message)
{
    unsigned long flag;
    spin_lock_irqsave(&(lock->spinlock), flag);
    if (lock->num_eng == 0)
    {
        spin_unlock_irqrestore(&(lock->spinlock), flag);
        return -1;
    }
    else
    {
        get_translation_in_english(message);
        lock->num_eng--;
        spin_unlock_irqrestore(&(lock->spinlock), flag);
        return 0;
    }
}

int martian_get_output(me_lock *lock, msg *message)
{
    unsigned long flag;
    spin_lock_irqsave(&(lock->spinlock), flag);
    if (lock->num_mar == 0)
    {
        spin_unlock_irqrestore(&(lock->spinlock), flag);
        return -1;
    }
    else
    {
        get_translation_in_martian(message);
        lock->num_mar--;
        spin_unlock_irqrestore(&(lock->spinlock), flag);
        return 0;
    }
}

/* 
Use these four routines to interface to the translation hardware and
queueing system.  Note that the translate_to routines do not check for
full output queues, nor do the get_transation routines check for 
empty queues.  None of the four routines should be called simultaneously
with any others (including themselves).

You do not need to define these functions, but you need to call them in 
your synchronization interface.
*/

/* 
 * translate_to_english
 *   DESCRIPTION: translate the message in the buffer to English;
 *      then put the message in the corresponding queue.
 *   INPUTS: message - a pointer to the input message buffer.
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECT: none
 */
void translate_to_english(msg *message);

/* 
 * translate_to_martian
 *   DESCRIPTION: translate the message in the buffer to Martian;
 *      then put the message in the corresponding queue.
 *   INPUTS: message - a pointer to the input message buffer.
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECT: none
 */
void translate_to_martian(msg *message);

/* 
 * get_translation_in_english
 *   DESCRIPTION: get a translated message in English.
 *   INPUTS: message - a pointer to the message buffer which will
 *      be filled in with a translated English message.
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECT: Will fill in the given message buffer.
 */
void get_translation_in_english(msg *message);

/* 
 * get_translation_in_martian
 *   DESCRIPTION: get a translated message in Martian.
 *   INPUTS: message - a pointer to the message buffer which will
 *      be filled in with a translated Martian message.
 *   OUTPUTS: none
 *   RETURN VALUE: none
 *   SIDE EFFECT: Will fill in the given message buffer.
 */
void get_translation_in_martian(msg *message);
