class InventoryUploadsController < ApplicationController
  def create # Handle POST /inventory_uploads.json
    batch_id = SecureRandom.uuid

    if inventory_params.is_a?(Array)
      created_units = []
      inventory_params.each do |unit|
	  # Create a record for each inventory unit
        created_unit = InventoryUnit.create(
          name: unit['name'],
          quantity: unit['quantity'].to_i,
          price: unit['price'].to_f,
          batch_id: batch_id
        )
        created_units << created_unit
      end

      if created_units.all?(&:persisted?) # Success response
        render json: { message: 'Inventory uploaded successfully', batch_id: batch_id }, status: :created
      else
        render json: { error: 'Failed to save some inventory units', details: created_units.map(&:errors) }, status: :unprocessable_entity # Error if any unit failed to save
      end
    else
      render json: { error: 'Invalid data format. Expected an array of inventory units.' }, status: :unprocessable_entity # Error if data is not an array
    end
  end

  def index # Handle GET /inventory_uploads.json
    batches = InventoryUnit.all.group_by(&:batch_id) # Group inventory units by batch_id
    result = batches.map do |batch_id, units| # Prepare summary data for each batch
      {
        batch_id: batch_id,
        number_of_units: units.count,
        average_price: (units.map(&:price).sum / units.count).round(2),
        total_quantity: units.map(&:quantity).sum
      }
    end

    render json: result, status: :ok
  end

  private

  def inventory_params # Strong parameters to permit an array of inventory units
    params.require(:_json)
  end
end
