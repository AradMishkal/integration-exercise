class InventoryUploadsController < ApplicationController
  def create
    batch_id = SecureRandom.uuid

    if inventory_params.is_a?(Array)
      created_units = []
	# Create an InventoryUnit for each uploaded item
      inventory_params.each do |unit|
        created_unit = InventoryUnit.create(
          name: unit['name'],
          quantity: unit['quantity'].to_i,
          price: unit['price'].to_f,
          batch_id: batch_id
        )
        created_units << created_unit
      end

      if created_units.all?(&:persisted?)
        render json: { message: 'Inventory uploaded successfully', batch_id: batch_id }, status: :created
      else
        render json: { error: 'Failed to save some inventory units', details: created_units.map(&:errors) }, status: :unprocessable_entity
      end
    else
      render json: { error: 'Invalid data format. Expected an array of inventory units.' }, status: :unprocessable_entity
    end
  end

  def index
    # Group all inventory units by their batch_id
    batches = InventoryUnit.all.group_by(&:batch_id)

    result = batches.map do |batch_id, units|
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

  def inventory_params
    params.require(:_json)
  end
end
