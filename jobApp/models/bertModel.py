from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch

# Load the pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Define your training and validation datasets
train_texts = [...]  # List of training texts
train_labels = [...]  # List of training labels (integers)
val_texts = [...]  # List of validation texts
val_labels = [...]  # List of validation labels (integers)

# Tokenize your texts and encode your labels as tensors
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)
train_labels = torch.tensor(train_labels)
val_labels = torch.tensor(val_labels)

# Define a function to format the data as PyTorch DataLoader objects
def create_data_loader(encodings, labels, batch_size):
    dataset = torch.utils.data.TensorDataset(
        torch.tensor(encodings['input_ids']),
        torch.tensor(encodings['attention_mask']),
        labels
    )
    return torch.utils.data.DataLoader(dataset, batch_size=batch_size)

# Define the training arguments, such as the number of epochs and the learning rate
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    learning_rate=5e-5,
    weight_decay=0.01,
    evaluation_strategy='epoch',
    save_total_limit=1,
    load_best_model_at_end=True,
    metric_for_best_model='accuracy',
)

# Instantiate a trainer and fine-tune the pre-trained BERT model on your dataset
trainer = Trainer(
    model=model,
    args=training_args,
    train_loader=create_data_loader(train_encodings, train_labels, batch_size=16),
    eval_loader=create_data_loader(val_encodings, val_labels, batch_size=64),
    compute_metrics=lambda pred: {'accuracy': (pred['labels'] == pred['predictions']).mean()},
)
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_bert')
