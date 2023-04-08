from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Load the pre-trained GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Load your dataset and preprocess it into a format suitable for training the language model
dataset = TextDataset(tokenizer=tokenizer, file_path='jobApp/data/dataset.txt', block_size=128)

# Define a data collator to handle batching and padding of the training examples
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define the training arguments, such as the number of epochs and the learning rate
training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    learning_rate=2e-5,
    save_steps=5000,
    save_total_limit=2,
    prediction_loss_only=True,
)

# Instantiate a trainer and fine-tune the pre-trained GPT-2 model on your dataset
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_gpt2')
